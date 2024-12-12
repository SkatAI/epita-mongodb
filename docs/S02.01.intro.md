# S02.01.intro

Last time we got acquainted with MongoDB on the Atlas hosting service

- Universe of databases
- Specifics of NoSQL
- Practiced some basic querying MongoDB with filters and projections

```javascript
db.movies.find(
    {runtime: {$gt : 180}},  // Filter on movie duration
    { _id: 0, title: 1, runtime: 1, "imdb.rating": 1 }  // Projection to include title and imdb.rating, exclude _id
)
```

## Today

Today we continue working with MongoDB

- aggregation pipelines
  - follow https://www.mongodb.com/docs/languages/python/pymongo-driver/current/aggregation/aggregation-tutorials/
- schema
  - schema validation
  - schema design - to optimize query time
  - collections, documents and embedded documents

And talk about

- data types + BSON + equivalence JSON
- transactions and ACID properties
- data modifications: partial updates ($set, $inc etc.) and Array operations
- and MongoDB Stored Procedures
- and index creation

## Practice

2 worksheets :

- write aggregation pipelines for complex queries on the movies dataset


- Paris trees dataset and geoJSON
  - import a dataset into a newly created database on the Paris trees
  - write the validation schema
  - convert geolocation strings into Point
  - Combine gardens and trees into a single collection




