# Short Course on NoSQL MongoDB

This is the repo for the course on advanced databases winter 2024.

This repo covers NoSQL and MongoDB

It is a work in progress. stay tuned.

The second part of the course which covers Neo4j is available at https://github.com/SkatAI/epita-neo4j


## Scope

### session_01: world of databases, and getting started on MongoDB


- title: 1.1 course welcome and logistics
  - course scope
  - evaluation
  - discord
  - office hours
  - get to know survey

- title: 1.2 A world of databases;
  - goal: clear picture of the what for why
  - desc: difference between sql, mongodb and graph, add vector
    - DBMS & history of databases
    - Types of databases
    - relational vs non relation database
    - flexible schema in NoSQL databases
    - graph databases
    - conclusion

- title: 1.3 guided practice - hands on with mongodb
  - goal: get started with mongodb as a datastore
  - desc: create a collection, insert and update some documents, run basic queries
    - understand diff of cluster location (local, cloud), CLI vs Compass vs CLI in Compass
    - [guided] open an account on Atlas
    - [guided] demo: how to query a mongodb database, load a dataset, some queries
  - practice: |
    - load and explore a small dataset (Movies).
    - answer set of questions



### session_02: Mongo Deeper Dive

- title: 2.01 last session recap
  - desc: recap of key points in last session - equivalence SQL vs NoSQL for querying
    - querying,
      - filtering
      - projection
    - key diffs in CRUD ops: `$lookup`, aggregation pipelines (GROUP BY), Nested/embedded documents
    - document validation

- title: 2.02 MongoDb aggregation pipelines
  - desc: More complex queries with aggregation pipelines
    - aggregation pipelines
    - $match, $group, $unwind, $addFields, $out
    - joins with $lookup

- title: 2.03 MongoDb deeper dive
  - desc: More complex queries with schema design and validation
    - how mongo shines: why and when to choose over sql
    - schema
      - schema design - to optimize query time
      - relations
      - schema validation
  - missing:
    - data types + BSON + equivalence JSON
    - transactions and ACID properties
    - data modifications: partial updates ($set, $inc etc.) and Array operations
    - MongoDB Stored Procedures

### session_03: Worksheet on Paris Trees

- title: 3.02 MongoDb trees worksheet
  - desc: Build a database of trees and gardens in Paris
    - loading data
    - aggregation queries
    - partial updates
    - schema design and validation
    - geoJSON conversion and spatial queries
  - quiz : <https://quiz.skatai.com/quiz/worksheet-on-paris-trees-data-in-mongodb>
