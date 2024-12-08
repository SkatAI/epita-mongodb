
db.getCollectionInfos({ name: "trees" });
db.trees.deleteMany({});

db.trees.drop();
db.getCollectionNames();

// --------------------------------------------------------------
// load the data within mongosh
// --------------------------------------------------------------
// use trees_flat_db
const fs = require("fs");

// Load and parse the JSON file
const dataPath = "./trees_flat_10K.json"
const treesData = JSON.parse(fs.readFileSync(dataPath, "utf8"));

// Insert data into the desired collection
db.trees.drop();
db.getCollectionNames();

let startTime = new Date()
db.trees.insertMany(treesData);
let endTime = new Date()
print(`Operation took ${endTime - startTime} milliseconds`)

// Operation took 42943 milliseconds
// Operation took 37191 milliseconds
// Operation took 41138 milliseconds

// --------------------------------------------------------------
// create the collection and the validator and load data within mongosh
// --------------------------------------------------------------

db.trees.drop()
db.getCollectionNames()

db.createCollection("trees", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["name", "height", "circumference"],
            properties: {
                name: {
                    bsonType: "string",
                    description: "Name must be a string and is required"
                },
                height: {
                    bsonType: "number",
                    minimum: 0,
                    maximum: 50,
                    description: "Height must be between 0 and 50"
                },
                circumference: {
                    bsonType: "number",
                    minimum: 0,
                    maximum: 500,
                    description: "Circumference must be between 0 and 500"
                }
            }
        }
    },
    validationAction: "error",  // Instead of error
});

// check validator
db.getCollectionInfos({ name: "trees" });

db.setProfilingLevel(2); // Logs all operations

// Insert data into the desired collection
let startTime = new Date()
db.trees.insertMany(treesData);
let endTime = new Date()
print(`Operation took ${endTime - startTime} milliseconds`)

// Operation took 43231 milliseconds

// --------------------------------------------------
// geolocation dups
// --------------------------------------------------


db.trees.aggregate([
    {
        $group: {
            _id: {
                geo_point_2d: "$geo_point_2d"
            },
            count: { $sum: 1 }, // Count the number of occurrences
            docs: { $push: "$_id" } // Collect document IDs for reference
        }
    },
    {
        $match: {
            count: { $gt: 1 } // Keep only groups with more than 1 document
        }
    },
    {
        $project: {
            _id: 0, // Exclude the _id field from the output
            geo_point_2d: "$_id.geo_point_2d",
            duplicateCount: "$count",
            documentIds: "$docs"
        }
    }
]);

//  finds 11 trees

// drop and recreate collection with validator

// and add unique index
db.trees.drop()
db.getCollectionNames()

db.createCollection("trees", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["name", "height", "circumference"],
            properties: {
                name: {
                    bsonType: "string",
                    description: "Name must be a string and is required"
                },
                height: {
                    bsonType: "number",
                    minimum: 0,
                    maximum: 50,
                    description: "Height must be between 0 and 50"
                },
                circumference: {
                    bsonType: "number",
                    minimum: 0,
                    maximum: 500,
                    description: "Circumference must be between 0 and 500"
                }
            }
        }
    },
    validationAction: "error",  // Instead of error
});

// create index
db.trees.createIndex({ "geo_point_2d": 1 }, { unique: true })

// show indexes

db.trees.getIndexes()


// -------------------------------------------------------
//  geojson location
// -------------------------------------------------------

db.trees.aggregate([
    // { $limit: 1000 },  // Get just 5 documents to work with
    {
        $addFields: {
            // Split the string into an array of [latitude, longitude]
            coordinates: {
                $map: {
                    input: { $split: ["$geo_point_2d", ", "] },
                    as: "coord",
                    in: { $toDouble: "$$coord" } // Convert to numbers
                }
            }
        }
    },
    {
        $addFields: {
            // Create a GeoJSON object with reordered coordinates [longitude, latitude]
            location_geojson: {
                type: "Point",
                coordinates: [
                    { $arrayElemAt: ["$coordinates", 1] }, // longitude
                    { $arrayElemAt: ["$coordinates", 0] }  // latitude
                ]
            }
        }
    },
    {
        $unset: "coordinates" // Optionally remove the intermediate array field
    },
    {
        $merge: {     // Or use $out if you want to create a new collection
            into: "trees",
            whenMatched: "merge",
            whenNotMatched: "discard"
        }
    }
]);