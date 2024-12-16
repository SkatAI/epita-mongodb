# CheatSheet Aggregation Pipelines MongoDB

## Dataset sample

Based on the trees dataset

```json
{
    "idbase": 227160,
    "domain": "Alignement",
    "dimensions": {
        "height": 15,
        "circumference": 165,
    },
    "location": {
        "id_location": "201008",
        "address": "PORT DES SAINTS PERES / QUAI MALAQUAIS",
        "arrondissement": "PARIS 6E ARRDT"
    },
    "geo": {
        "geo_point_2d": "48.85831741176347, 2.3344414199576278"
    },
    "taxonomy": {
        "name": "Peuplier",
        "species": "alba",
        "genre": "Populus",
        "variety": "Raket"
    }
}
```

## Basic Syntax

```javascript
db.collection.aggregate([
    { stage1 },
    { stage2 },
    ...
])
```

## Essential Operators

### $match - Filtering

```javascript
// Basic filtering
{ $match: { height: { $gt: 10 } } }

// Multiple conditions
{ $match: {
    $and: [
        { domain: "Jardin" },
        { "dimensions.height": { $gte: 5 } }
    ]
}}
```

### $set/$addFields - Add New Fields

```javascript
// Add single field
{ $set: {
    heightInFeet: { $multiply: ["$height", 3.28084] }
}}

// Add multiple fields
{ $addFields: {
    fullSpecies: { $concat: ["$taxonomy.genre", " ", "$taxonomy.species"] },
    isLarge: { $gte: ["$dimensions.height", 15] }
}}
```

### $project - Shape Output

```javascript
// Include/exclude fields
{ $project: {
    _id: 0,
    name: 1,
    location: 1
}}

// Rename and compute
{ $project: {
    treeName: "$taxonomy.name",
    location: {
        district: "$location.arrondissement",
        coordinates: "$location.geo_point_2d"
    }
}}
```

### $sort and $limit - Order and Slice

```javascript
// Sort (1: ascending, -1: descending)
{ $sort: { "dimensions.height": -1 } }

// Limit results
{ $limit: 10 }
```

### $group - Aggregation

```javascript
// Basic grouping
{ $group: {
    _id: "$taxonomy.genre",
    count: { $sum: 1 },
    avgHeight: { $avg: "$dimensions.height" },
    maxCircumference: { $max: "$dimensions.circumference" }
}}

// Multiple group levels
{ $group: {
    _id: {
        genre: "$taxonomy.genre",
        district: "$location.arrondissement"
    },
    trees: { $push: "$$ROOT" }
}}
```


### Array Operations

```javascript
// Unwind arrays
{ $unwind: "$arrayField" }

// Filter arrays
{ $filter: {
    input: "$arrayField",
    as: "item",
    cond: { $gt: ["$$item.value", 10] }
}}
```

### Lookup (Joins)

```javascript
{ $lookup: {
    from: "otherCollection",
    localField: "fieldA",
    foreignField: "fieldB",
    as: "joinedData"
}}
```

### Conditional Logic

```javascript
// Switch-case style
{ $switch: {
    branches: [
        { case: { $gt: ["$height", 20] }, then: "Tall" },
        { case: { $gt: ["$height", 10] }, then: "Medium" }
    ],
    default: "Small"
}}

// If-then-else
{ $cond: [
    { $gt: ["$dimensions.height", 15] },
    "Large",
    "Small"
]}
```