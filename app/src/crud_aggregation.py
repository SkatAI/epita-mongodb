# guided practice Atlas sample dataset

import os
import json
from pymongo import MongoClient

def connect_to_atlas(connection_string):
    """
    Connect to a MongoDB Atlas cluster.

    Args:
        connection_string (str): Your MongoDB Atlas connection string.

    Returns:
        MongoClient: The MongoDB client instance.
    """
    try:
        client = MongoClient(connection_string)
        # Test the connection
        client.admin.command('ping')
        print("Connected to MongoDB Atlas successfully!")
        return client
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":


    connection_string = os.getenv("MONGO_ATLAS_URI")

    client = connect_to_atlas(connection_string)

    # Example usage: Access a database and collection
    if not client:
        raise "Error connecting"

    # connect to database and get the movies collection
    db = client["sample_mflix"]
    collection = db["movies"]

    # method `find_one`

    print("Here is one document from the movies collection")
    res = collection.find_one()
    # default=str solves the: TypeError: Object of type ObjectId is not JSON serializable
    print(json.dumps(res, default=str, indent = 4))

    # aggregation
    # https://pymongo.readthedocs.io/en/stable/examples/aggregation.html


    '''
    Now that we cna connect, let's delete our small misic dataset

    person_coll.delete_many({})

    '''
    db = client["musicdb"]
    music_coll = db["music"]

    music_coll.delete_many({})

    # check that we have 0 documents
    assert music_coll.count_documents({}) == 0


    '''
    - count? to check
    - how to close connection
    '''

    # Let's go back to mflix db
    db = client["sample_mflix"]
    collection = db["movies"]

    # create a pipeline
    pipeline = []

    # then add a filter with match
    # movies of a minimum duration runtime
    # see $gt https://www.mongodb.com/docs/manual/reference/operator/query/gt/

    pipeline.append({
        "$match": {
            "runtime": { "$gt" : 120}
        }
    })

    # add sort with descending order
    pipeline.append({
        "$sort": {
            "released": -1
        }
    })

    # than add a limit to only get the top 3 movies
    pipeline.append({
        "$limit": 3
    })

    # also we don't want _id, plot or full_plot

    # pipeline lookks like this
    # Out[29]: [{'$match': {'year': '2000'}}, {'$sort': {'released': -1}}, {'$limit': 3}]

    pipeline.append({
        "$unset": [
            "_id",
            "plot",
            "fullplot",
        ]
    })

    res = collection.aggregate(pipeline)

    # res is a command cursor
    for doc in res:
        print(doc)
    # or
    print(res.to_list())

    # the query equivalent to the pipeline is

    res = db.collection.find(
        {'runtime': {'$gt': 120}},  # Equivalent to the $match stage
        {'_id': 0, 'plot': 0, 'fullplot': 0}  # Equivalent to the $unset stage
    ).sort(
        'released', -1  # Equivalent to the $sort stage
    ).limit(3)  # Equivalent to the $limit stage

    # distinct


    # group

    finding movies with weird years using regex
    # cursor = db.movies.find({"year": {"$regex": "è"}})

