import pandas as pd

pd.options.display.max_columns = 1000
pd.options.display.width = 150

import os
from tqdm import tqdm
import numpy as np

import re
import unicodedata
import json

def clean_string(input_string):
    # Convert to lowercase
    cleaned = input_string.lower()
    # Remove "l'" and "d'"
    cleaned = re.sub(r"\bl'|\bd'", "", cleaned)
    # Normalize and remove accents
    cleaned = ''.join(
        char for char in unicodedata.normalize('NFD', cleaned)
        if unicodedata.category(char) != 'Mn'
    )
    # Replace spaces with underscores
    cleaned = cleaned.replace(" ", "_")
    # Keep only letters, digits, and underscores
    cleaned = re.sub(r"[^a-z0-9_]", "", cleaned)
    # Remove consecutive underscores
    cleaned = re.sub(r"_{2,}", "_", cleaned)
    # Remove leading or trailing underscores
    cleaned = cleaned.strip("_")

    return cleaned

def build(fields, some_dict, data):

    for col in fields:
        value = data[col]
        if not (value is None or (isinstance(value, float) and np.isnan(value))):
            some_dict[col] = value
    return some_dict




if __name__ == "__main__":

    # load the csv file into a dataframe
    file = './data-local/les_arbres_upload_v02.csv'
    df = pd.read_csv(file)


    # make sure duplicates geolocs are included
    # sort to show geo dups and large trees first. useful for detecting outliers in small sets

    df['dim'] = df.height * df.circumference
    df['geo_dups'] = df['geo_point_2d'].map(
        df['geo_point_2d'].value_counts()
    )

    df.sort_values(by = ['geo_dups','dim'], ascending=[False, False] , inplace = True)

    df.drop(columns= ['geo_dups','dim'], inplace = False)


    df['remarkable'] = df.remarkable.apply(lambda d : np.nan if d == 'NON' else d)

    cond = ~df['arrondissement'].isin(['BOIS DE BOULOGNE','BOIS DE VINCENNES','HAUTS-DE-SEINE','SEINE-SAINT-DENIS','VAL-DE-MARNE'])
    df = df[cond].copy()

    df.reset_index(inplace = True, drop = True)

    # --------------------------------------------------------
    # nested schema
    # --------------------------------------------------------

    # fields
    base_fields = ['idbase', 'domain', 'stage', 'remarkable', 'height', 'circumference']
    location_fields = [ 'id_location', 'suppl_address', 'number', 'address', 'arrondissement']
    geo_fields = [ 'geo_point_2d']
    taxonomy_fields = ['name', 'species', 'genre', 'variety']

    trees_nested = []
    for i, d in tqdm(df.iterrows()):
        tree = build(base_fields, {}, d)

        tree['location'] = build(location_fields, {}, d)

        tree['geo'] = build(geo_fields, {}, d)

        tree['taxonomy'] = build(taxonomy_fields, {}, d)
        trees_nested.append(tree)

    # save

    output_file = "./data/trees.json"
    with open(output_file, "w") as f:
        json.dump(trees_nested, f, indent=4,  ensure_ascii=False)
    print(f"created {output_file}")

    output_file = "./data/trees_100.json"
    with open(output_file, "w") as f:
        json.dump(trees_nested[:100], f, indent=4,  ensure_ascii=False)
    print(f"created {output_file}")

    output_file = "./data/trees_1k.json"
    with open(output_file, "w") as f:
        json.dump(trees_nested[:1000], f, indent=4,  ensure_ascii=False)

    print(f"created {output_file}")

    # convert to ndjson (useful for mongoimport and smaller size)
    print("-- convert to ndjson")
    with open("./data/trees.json", "r") as infile, open("./data/trees.ndjson", "w") as outfile:
        data = json.load(infile)
        for item in tqdm(data):
            outfile.write(json.dumps(item) + "\n")



    # --------------------------------------------------------
    # gardens
    # --------------------------------------------------------
    print("==")
    print("Gardens")

    df = pd.read_csv('./data-local/espaces_verts.csv', sep = ';')
    df.columns = [clean_string(col) for col in df.columns]

    df.dropna(subset = ['code_postal'], inplace = True )

    df['code_postal'] = df.code_postal.astype(int)

    df.drop(columns= ['last_edited_user', 'last_edited_date', 'url_plan', 'competence'], inplace = True)

    df.rename(columns = {
        'identifiant_espace_vert': 'identifiant',
        'nom_de_espace_vert': 'nom', 'typologie_espace_vert': 'typologie', 'presence_cloture': 'cloture', 'ancien_nom_de_espace_vert': 'ancien_nom'},
        inplace = True
        )

    df.reset_index(inplace = True, drop = True)

    # fields
    base_fields = ['nom', 'typologie', 'categorie','cloture','nombre_entites', 'ouverture_24h_24h',]
    location_fields = [ 'adresse_numero', 'adresse_complement', 'adresse_type_voie', 'adresse_libelle_voie', 'code_postal']
    surface_fields = [ 'surface_calculee', 'superficie_totale_reelle', 'surface_horticole', 'perimetre' ]
    history_fields = [ 'annee_de_ouverture', 'annee_de_renovation', 'ancien_nom', 'annee_de_changement_de_nom']
    geo_fields = [ 'geo_shape', 'geo_point']
    identification_fields = ['identifiant', 'id_division', 'id_atelier_horticole', 'ida3d_enb', 'site_villes', 'id_eqpt' ]

    # jsonsify without nulls
    gardens = []

    for i, d in tqdm(df.iterrows()):
        garden = build(df.columns, {}, d)

        garden = build(base_fields, {}, d)
        garden['id'] = build(identification_fields, {}, d)
        garden['location'] = build(location_fields, {}, d)
        garden['surface'] = build(surface_fields, {}, d)
        garden['history'] = build(history_fields, {}, d)
        garden['geo'] = build(geo_fields, {}, d)

        gardens.append(garden)

    # convert geo_shape
    for garden in gardens:
        garden['geo']['geo_shape'] = json.loads(garden['geo']['geo_shape'])

    output_file = "./data/gardens.json"
    with open(output_file, "w") as f:
        json.dump(gardens, f, indent=4,  ensure_ascii=False)

    print(f"created {output_file}")


    output_file = "./data/gardens_100.json"
    with open(output_file, "w") as f:
        json.dump(gardens[:100], f, indent=4,  ensure_ascii=False)
    print(f"created {output_file}")

    output_file = "./data/gardens_1k.json"
    with open(output_file, "w") as f:
        json.dump(gardens[:1000], f, indent=4,  ensure_ascii=False)

    print(f"created {output_file}")

    # convert to ndjson (useful for mongoimport and smaller size)
    print("-- convert to ndjson")
    with open("./data/gardens.json", "r") as infile, open("./data/gardens.ndjson", "w") as outfile:
        data = json.load(infile)
        for item in tqdm(data):
            outfile.write(json.dumps(item) + "\n")


