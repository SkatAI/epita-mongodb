import pandas as pd
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

    # file = './data/les_arbres_upload_1k.csv'
    file = './data/les_arbres_upload_v02.csv'
    # load the csv file into a dataframe
    df = pd.read_csv(file)

    # --------------------------------------------------------
    # flat schema
    # --------------------------------------------------------
    trees = []

    for i, d in tqdm(df.iterrows()):
        tree = build(df.columns, {}, d)
        trees.append(tree)

    # create json filename by replacing .csv with .json
    output_file = "./data/trees_flat.json"
    with open(output_file, "w") as f:
        json.dump(trees, f, indent=4,  ensure_ascii=False)

    output_file = "./data/trees_flat_1K.json"
    with open(output_file, "w") as f:
        json.dump(trees[:1000], f, indent=4,  ensure_ascii=False)

    output_file = "./data/trees_flat_100.json"
    with open(output_file, "w") as f:
        json.dump(trees[:100], f, indent=4,  ensure_ascii=False)

    # convert to ndjson

    with open("./data/trees_flat.json", "r") as infile, open("trees_flat.ndjson", "w") as outfile:
        data = json.load(infile)
        for item in data:
            outfile.write(json.dumps(item) + "\n")



    # --------------------------------------------------------
    # nested schema
    # --------------------------------------------------------
    df['remarkable'] = df.remarkable.apply(lambda d : np.nan if d == 'NON' else d)

    # fields
    base_fields = ['idbase', 'domain', 'stage', 'remarkable']
    location_fields = ['arrondissement', 'suppl_address', 'number', 'address', 'id_location', 'geo_point_2d']
    metrics_fields = ['height', 'circumference']
    taxonomy_fields = ['name', 'species', 'genre', 'variety']


    trees_nested = []
    for i, d in tqdm(df.iterrows()):
        tree = build(base_fields, {}, d)

        tree['location'] = build(location_fields, {}, d)


        tree['dimensions'] = build(metrics_fields, {}, d)

        tree['taxonomy'] = build(taxonomy_fields, {}, d)
        trees_nested.append(tree)

    # save to

    output_file = "./data/trees_nested.json"
    with open(output_file, "w") as f:
        json.dump(trees_nested, f, indent=4,  ensure_ascii=False)

    output_file = "./data/trees_nested_1k.json"
    with open(output_file, "w") as f:
        json.dump(trees_nested[:1000], f, indent=4,  ensure_ascii=False)

    output_file = "./data/trees_nested_100.json"
    with open(output_file, "w") as f:
        json.dump(trees_nested[:100], f, indent=4,  ensure_ascii=False)

    with open("./data/trees_nested.json", "r") as infile, open("trees_nested.ndjson", "w") as outfile:
        data = json.load(infile)
        for item in data:
            outfile.write(json.dumps(item) + "\n")



    # --------------------------------------------------------
    # gardens
    # --------------------------------------------------------

    df = pd.read_csv('./data/espaces_verts.csv', sep = ';')
    df.columns = [clean_string(col) for col in df.columns]

    # jsonsify without nulls
    gardens = []

    for i, d in tqdm(df.iterrows()):
        garden = build(df.columns, {}, d)
        gardens.append(garden)

    output_file = "./data/gardens_001.json"
    with open(output_file, "w") as f:
        json.dump(gardens, f, indent=4,  ensure_ascii=False)




