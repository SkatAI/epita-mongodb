---
concept: Cluster > Database > Collection > Document
connection: connecting to a cluster
    different tools to work with mongodb: CLI and Compass
    different cluster location: local or cloud atlas
languages: working with mongodb in different langages from python to whatever
---

# MongoDB



## Get started

Part 2: Create Your First Collection (10 minutes)
Let's create a fun little music playlist database!

In Compass:

Click "Create Database"
Database name: music_db
Collection name: songs

Open Terminal/Command Prompt and run:
// Connect to MongoDB
mongosh

// Switch to our database
use music_db

// Insert your first song
db.songs.insertOne({
    title: "Happy",
    artist: "Pharrell Williams",
    year: 2013,
    mood: "joyful",
    lastPlayed: new Date()
})

Add a few more songs using Compass's interface:

db.songs.insertOne({
    "title": "Don't Stop Believin'",
    "artist": "Journey",
    "year": 1981,
    "mood": "inspiring",
    "lastPlayed": new Date()
})

Try these commands in mongosh:

Find all songs:

db.songs.find()

db.songs.find({ year: { $lt: 2000 } })

db.songs.countDocuments()

In Compass to add a record put the fields after the {_id}

```json
{
  "_id": {
    "$oid": "673f1f5b2adc93eb7abc7598"
  },
  "title": "Don't Stop Believin'",
  "artist": "Journey",
  "year": 1981,
  "mood": "inspiring",
  "lastPlayed": new Date()
}
```

```json
{
  "_id":{
    "$oid":"6745ab6f0e0bbdab062667c7"
    },
    "title": "Happy",
    "artist": "Pharrell Williams",
    "year": 2013,
    "mood": "joyful"
}
```

In compass query is also a json object


see <https://chatgpt.com/c/673f286f-3c44-800e-a533-7df1cb8d9da3>

## Querying

key equivalents between Mongodb and SQL

SELECT * FROM users

db.users.find()

SELECT * FROM users WHERE age = 21

db.users.find({ age: 21 })

SELECT name, age FROM users

db.users.find({}, { name: 1, age: 1 })

SELECT * FROM users WHERE age > 21 ORDER BY name ASC
db.users.find({ age: { $gt: 21 }}).sort({ name: 1 })

INSERT INTO users(name, age) VALUES ("John", 25)
db.users.insertOne({ name: "John", age: 25 })

UPDATE users SET age = 26 WHERE name = "John"
db.users.updateOne({ name: "John" }, { $set: { age: 26 }})

DELETE FROM users WHERE name = "John"
db.users.deleteOne({ name: "John" })

-- multiple rows

-- SQL Multiple Records
SELECT * FROM users WHERE age > 25;
UPDATE users SET status = 'active' WHERE city = 'Paris';
DELETE FROM users WHERE lastLogin < '2023-01-01';
INSERT INTO users (name, age) VALUES ('John', 25), ('Jane', 30);

becomes

// MongoDB Multiple Documents
db.users.find({ age: { $gt: 25 }});

db.users.updateMany(
  { city: "Paris" },
  { $set: { status: "active" }}
);

db.users.deleteMany({
  lastLogin: { $lt: new Date('2023-01-01') }
});

db.users.insertMany([
  { name: "John", age: 25 },
  { name: "Jane", age: 30 }
]);

=> TODO exercise on simple dataset

### differences between SQL and MongoDB queries

Complex queries:

SQL JOINs vs MongoDB $lookup behave differently
Nested/embedded documents in MongoDB have no direct SQL equivalent
MongoDB aggregation pipeline syntax differs significantly from SQL GROUP BY

Transaction handling:

MongoDB's transaction model is more limited than SQL
ACID properties are handled differently

Data modification:

MongoDB allows partial updates more naturally ($set, $inc etc.)
Array operations in MongoDB have no direct SQL equivalent
