'''
queries soltion to S01.03.mongodb-atlas.md
'''

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# connect to sample_mflix
connection_string = os.getenv('MONGO_ATLAS_URI')
client = MongoClient(connection_string)
db = client["sample_mflix"]
collection = db["movies"]


def query(filter, projection):
    print("--"*20)
    print(f"filter: {filter}")
    print(f"projection: {projection}")
    count = db.movies.count_documents(filter)

    print(f"\nThis returns {count} documents")
    print("\n-- here are the 5 first documents")
    cursor = db.movies.find( filter, projection).limit(5)
    for movie in cursor:
        print(movie)


# ---------------------
print("1. Retrieve all movies that have the genre 'Action'. return title and genres")

filter = {"genres": "Action"}
projection = {"_id": 0, "title": 1, "genres": 1}

query(filter, projection)


# ---------------------
print("2. Find Movies with an IMDb Rating Greater Than 8")

filter = {"imdb.rating": {"$gt": 7.0}}
projection = {"_id": 0, "title": 1, "imdb.rating": 1}
query(filter, projection)

# ---------------------
print("3. Retrieve movies released after the year 2000, showing only the title and release year.")

filter =    {"year": {"$gt": 2000}}
projection =     {"_id": 0, "title": 1, "year": 1}
query(filter, projection)

# ---------------------
print("4. Find movies directed by 'Christopher Nolan', showing the title, director, and year.")

filter= {"directors": "Christopher Nolan"}
projection =    {"_id": 0, "title": 1, "directors": 1, "year": 1}
query(filter, projection)

# ---------------------
print("5. Retrieve movies with a `tomatoes.viewer.rating` greater than `4.0`, showing the title and viewer rating.")

filter =  {"tomatoes.viewer.rating": {"$gt": 4.0}}
projection =    {"_id": 0, "title": 1, "tomatoes.viewer.rating": 1}
query(filter, projection)

# ---------------------
print("6. Find movies that contain `Comedy` and `Drama` in the `genres` array.")

filter = {"genres": {"$all": ["Comedy", "Drama"]}}
projection =   {"_id": 0, "title": 1, "genres": 1}
query(filter, projection)


# ---------------------
print("7. Retrieve movies where `Tom Hanks` is part of the cast.")

filter = {"cast": "Tom Hanks"}
projection =     {"_id": 0, "title": 1, "cast": 1}
query(filter, projection)

# ---------------------
print("8. Combine Query with Sorting: Retrieve the worst 5 movies with the lowest IMDb rating, showing title and rating.")

cursor = db.movies.find(
    {"imdb.rating": { "$type": "double" } },  # No filter: query all movies
    {"_id": 0, "title": 1, "imdb": 1}  # Projection: include title and IMDb rating
).sort("imdb.rating", -1).limit(5)  # Sort by IMDb rating (ascending) and limit to 5 results

for movie in cursor:
    print(movie)

# ---------------------
print("9. Query Movies with a Range of Years: Retrieve movies released between 1990 and 2000, showing the title and year.")

filter =  {"year": {"$gte": 1990, "$lte": 2000}}
projection =    {"_id": 0, "title": 1, "year": 1}
query(filter, projection)

# ---------------------
print("10. Query Movies with Missing Fields: Find movies where the `fullplot` field does not exist.")

filter =  {"fullplot": {"$exists": True}}
filter =  {"fullplot": {"$exists": False}}

projection =     {"_id": 0, "title": 1, "plot": 1, "fullplot": 1}
query(filter, projection)



