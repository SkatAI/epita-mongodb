
next : https://www.mongodb.com/docs/languages/python/pymongo-driver/current/aggregation/aggregation-tutorials/unpack-arrays/

there are multiple arryas in the movies collection

genres
cast
languages
writers
countries

and 3 embedded documents: awards, imdb & tomatoes

'awards': {'wins': 0, 'nominations': 1, 'text': '1 nomination.'},
'imdb': {'rating': 8.2, 'votes': 6, 'id': 1541777},
'tomatoes': {'viewer': {'rating': 0.5, 'numReviews': 13},

let's see how we can query the array fields

with the $unwind operator

pipeline.append({
    "$unwind": {
        "path": "$genres"
    }
})

to query over an emebedeed document we use the dot syntax: `imdb.rating`, `tomatoes.viewer.numReviews`
MongoDB allows you to reference deeply nested fields directly in queries.

for instance

db.movies.aggregate([
    { "$match": { "imdb.rating": { "$gt": 8.0 } } },
    { "$sort": { "imdb.rating": -1 } }  // Sort by rating in descending order
])

If you want to query movies and return only the imdb field:
db.movies.find({"imdb.rating": 8.2}, {"imdb": 1, "_id": 0})

db.movies.find({"tomatoes.viewer.rating": 0.5})
db.movies.find({"tomatoes.viewer.rating": {"$gt": 4.0}})

and with logical oprators

To find movies where:

    imdb.rating is greater than 8.0, OR
    imdb.votes is less than 10

Use the $or operator:

db.movies.find({
    "$or": [
        {"imdb.rating": {"$gt": 8.0}},
        {"imdb.votes": {"$lt": 10}}
    ]
})

### let's do it

Find movies with imdb.rating greater than 7.0 and sort them by tomatoes.viewer.rating in descending order:

db.movies.aggregate([
    { "$match": { "imdb.rating": { "$gt": 7.0 } } },
    { "$sort": { "tomatoes.viewer.rating": -1 } }
])

Group movies by tomatoes.viewer.rating and count the number of movies for each rating:

db.movies.aggregate([
    { "$group": {
        "_id": "$tomatoes.viewer.rating",
        "movie_count": { "$sum": 1 }
    }},
    { "$sort": { "_id": 1 } }
])

Compute the average imdb.rating for movies with more than 50 tomatoes.viewer.numReviews:

db.movies.aggregate([
    { "$match": { "tomatoes.viewer.numReviews": { "$gt": 50 } } },
    { "$group": {
        "_id": null,
        "average_imdb_rating": { "$avg": "$imdb.rating" }
    }}
])


Find movies where tomatoes.viewer.numReviews exists:

db.movies.aggregate([
    { "$match": { "tomatoes.viewer.numReviews": { "$exists": true } } }
])


amny other examples

Here’s a list of questions and their corresponding aggregation pipelines that demonstrate querying on nested fields in the `movies` collection using **aggregation pipelines**.

---

### **Basic Match Queries**
1. **Find all movies where `tomatoes.viewer.rating` is greater than `4.5`:**
   ```javascript
   db.movies.aggregate([
       { "$match": { "tomatoes.viewer.rating": { "$gt": 4.5 } } }
   ])
   ```

2. **Find movies where `imdb.rating` is greater than `8.0` and `tomatoes.viewer.rating` is greater than `3.5`:**
   ```javascript
   db.movies.aggregate([
       { "$match": {
           "imdb.rating": { "$gt": 8.0 },
           "tomatoes.viewer.rating": { "$gt": 3.5 }
       }}
   ])
   ```

---

### **Projection of Nested Fields**
3. **Find movies with `tomatoes.viewer.rating` greater than `4.0` and return only `title`, `imdb.rating`, and `tomatoes.viewer`:**
   ```javascript
   db.movies.aggregate([
       { "$match": { "tomatoes.viewer.rating": { "$gt": 4.0 } } },
       { "$project": { "title": 1, "imdb.rating": 1, "tomatoes.viewer": 1, "_id": 0 } }
   ])
   ```

---

### **Sorting**
4. **Find movies with `imdb.rating` greater than `7.0` and sort them by `tomatoes.viewer.rating` in descending order:**
   ```javascript
   db.movies.aggregate([
       { "$match": { "imdb.rating": { "$gt": 7.0 } } },
       { "$sort": { "tomatoes.viewer.rating": -1 } }
   ])
   ```

---

### **Group and Aggregate**
5. **Group movies by `tomatoes.viewer.rating` and count the number of movies for each rating:**
   ```javascript
   db.movies.aggregate([
       { "$group": {
           "_id": "$tomatoes.viewer.rating",
           "movie_count": { "$sum": 1 }
       }},
       { "$sort": { "_id": 1 } }
   ])
   ```

6. **Compute the average `imdb.rating` for movies with more than `50` `tomatoes.viewer.numReviews`:**
   ```javascript
   db.movies.aggregate([
       { "$match": { "tomatoes.viewer.numReviews": { "$gt": 50 } } },
       { "$group": {
           "_id": null,
           "average_imdb_rating": { "$avg": "$imdb.rating" }
       }}
   ])
   ```

---

### **Array Aggregation**
7. **Create an array of all unique `imdb.rating` values for movies with `tomatoes.viewer.rating` greater than `3.0`:**
   ```javascript
   db.movies.aggregate([
       { "$match": { "tomatoes.viewer.rating": { "$gt": 3.0 } } },
       { "$group": {
           "_id": null,
           "unique_imdb_ratings": { "$addToSet": "$imdb.rating" }
       }}
   ])
   ```

---

### **Bucketization**
8. **Bucket movies by `tomatoes.viewer.rating` into ranges and count how many fall into each range:**
   ```javascript
   db.movies.aggregate([
       { "$bucket": {
           "groupBy": "$tomatoes.viewer.rating",
           "boundaries": [0, 2, 4, 6, 8, 10],
           "default": "Other",
           "output": { "movie_count": { "$sum": 1 } }
       }}
   ])
   ```

---

### **Filtering Arrays in Nested Fields**
9. **Find movies where any value in `tomatoes.critic.reviews` matches "Excellent":**
   ```javascript
   db.movies.aggregate([
       { "$match": { "tomatoes.critic.reviews": "Excellent" } }
   ])
   ```

---

### **Add Computed Fields**
10. **Add a computed field that calculates the difference between `imdb.rating` and `tomatoes.viewer.rating`:**
    ```javascript
    db.movies.aggregate([
        { "$project": {
            "title": 1,
            "imdb.rating": 1,
            "tomatoes.viewer.rating": 1,
            "rating_difference": { "$subtract": ["$imdb.rating", "$tomatoes.viewer.rating"] }
        }}
    ])
    ```

---

### **Nested Logical Conditions**
11. **Find movies where `imdb.rating` is greater than `8.0` OR `tomatoes.viewer.rating` is less than `2.0`:**
    ```javascript
    db.movies.aggregate([
        { "$match": {
            "$or": [
                { "imdb.rating": { "$gt": 8.0 } },
                { "tomatoes.viewer.rating": { "$lt": 2.0 } }
            ]
        }}
    ])
    ```

12. **Find movies where `imdb.rating` is between `7.0` and `9.0`, and `tomatoes.viewer.numReviews` is greater than `100`:**
    ```javascript
    db.movies.aggregate([
        { "$match": {
            "imdb.rating": { "$gte": 7.0, "$lte": 9.0 },
            "tomatoes.viewer.numReviews": { "$gt": 100 }
        }}
    ])
    ```

---

### **Pipeline with $setWindowFields**
13. **Calculate a running average of `imdb.rating` for movies sorted by `tomatoes.viewer.numReviews`:**
    ```javascript
    db.movies.aggregate([
        { "$setWindowFields": {
            "sortBy": { "tomatoes.viewer.numReviews": 1 },
            "output": {
                "running_avg_rating": {
                    "$avg": "$imdb.rating",
                    "window": { "documents": ["unbounded", "current"] }
                }
            }
        }}
    ])
    ```

---

### **Existence Check**
14. **Find movies where `tomatoes.viewer.numReviews` exists:**
    ```javascript
    db.movies.aggregate([
        { "$match": { "tomatoes.viewer.numReviews": { "$exists": true } } }
    ])
    ```

15. **Find movies where `imdb.votes` does not exist:**
    ```javascript
    db.movies.aggregate([
        { "$match": { "imdb.votes": { "$exists": false } } }
    ])
    ```

---

### **Type Check**
16. **Find movies where `imdb.rating` is a string (to detect schema inconsistencies):**
    ```javascript
    db.movies.aggregate([
        { "$match": { "imdb.rating": { "$type": "string" } } }
    ])
    ```



#### Lookups


The `$lookup` stage in MongoDB allows you to perform a left outer join between two collections. In the **Atlas sample dataset `sample_mflix`**, you can use `$lookup` to combine data across collections like `movies`, `comments`, `users`, and `theaters`.

Here are a few examples:

---

### 1. **Join Movies with Comments**
Find all comments for each movie.

```javascript
db.movies.aggregate([
    {
        "$lookup": {
            "from": "comments",           // Collection to join
            "localField": "_id",          // Field in the `movies` collection
            "foreignField": "movie_id",   // Field in the `comments` collection
            "as": "movie_comments"        // Output array field
        }
    },
    {
        "$project": { "title": 1, "movie_comments": 1 }  // Project relevant fields
    }
])
```

**Explanation**:
- Joins `movies` with `comments` where the `_id` in `movies` matches `movie_id` in `comments`.
- Creates an array `movie_comments` containing all comments for each movie.

---

### 2. **Join Comments with Users**
Find the user details for each comment.

```javascript
db.comments.aggregate([
    {
        "$lookup": {
            "from": "users",            // Collection to join
            "localField": "email",      // Field in the `comments` collection
            "foreignField": "email",    // Field in the `users` collection
            "as": "user_details"        // Output array field
        }
    },
    {
        "$project": { "text": 1, "user_details": 1 }  // Project relevant fields
    }
])
```

**Explanation**:
- Joins `comments` with `users` where the `email` fields match.
- Returns the comment text and corresponding user details.

---

### 3. **Find Movies with Their Theaters**
For each movie, find theaters showing it (assuming there's a connection based on some shared field, e.g., location or zip code).

```javascript
db.movies.aggregate([
    {
        "$lookup": {
            "from": "theaters",            // Collection to join
            "localField": "theater_ids",   // Field in `movies` (e.g., an array of theater IDs)
            "foreignField": "_id",         // Field in `theaters` collection
            "as": "theater_details"        // Output array field
        }
    },
    {
        "$project": { "title": 1, "theater_details": 1 }
    }
])
```

**Explanation**:
- Joins `movies` with `theaters` using a hypothetical `theater_ids` field in the `movies` collection.

---

### 4. **Find Users Who Commented on a Specific Movie**
List all users who have commented on a particular movie, e.g., "The Godfather".

```javascript
db.comments.aggregate([
    {
        "$match": { "movie_id": ObjectId("573a1390f29313caabcd4323") }  // Match specific movie
    },
    {
        "$lookup": {
            "from": "users",            // Collection to join
            "localField": "email",      // Field in `comments`
            "foreignField": "email",    // Field in `users`
            "as": "user_details"        // Output array field
        }
    },
    {
        "$project": { "text": 1, "user_details": 1 }  // Include relevant fields
    }
])
```

**Explanation**:
- Matches comments for the specified movie.
- Joins with `users` to get the details of the users who commented.

---

### 5. **Join Theaters with Their Locations**
Retrieve detailed location information for each theater.

```javascript
db.theaters.aggregate([
    {
        "$lookup": {
            "from": "locations",        // Hypothetical collection for locations
            "localField": "location.address.zipcode",  // Nested field in `theaters`
            "foreignField": "zipcode",                 // Field in `locations`
            "as": "location_details"                  // Output array field
        }
    },
    {
        "$project": { "theaterId": 1, "location_details": 1 }
    }
])
```

**Explanation**:
- Joins `theaters` with `locations` based on `zipcode`.
- Includes the location details for each theater.

---

### 6. **Aggregate Ratings for Movies with User Details**
Find the average rating for each movie along with user details who rated them.

```javascript
db.comments.aggregate([
    {
        "$group": {                      // Group comments by movie
            "_id": "$movie_id",
            "average_rating": { "$avg": "$rating" },
            "total_reviews": { "$sum": 1 }
        }
    },
    {
        "$lookup": {                     // Join with movies collection
            "from": "movies",
            "localField": "_id",
            "foreignField": "_id",
            "as": "movie_details"
        }
    },
    {
        "$unwind": "$movie_details"      // Unwind to make it a single document per movie
    },
    {
        "$project": {                    // Project relevant fields
            "movie_details.title": 1,
            "average_rating": 1,
            "total_reviews": 1
        }
    }
])
```

**Explanation**:
- Calculates average ratings for each movie.
- Joins with `movies` to get the title of each movie.

---

### 7. **Find Comments for Movies Directed by a Specific Director**
Find all comments on movies directed by "Christopher Nolan."

```javascript
db.movies.aggregate([
    {
        "$match": { "directors": "Christopher Nolan" }  // Match director
    },
    {
        "$lookup": {
            "from": "comments",
            "localField": "_id",
            "foreignField": "movie_id",
            "as": "comments"
        }
    },
    {
        "$project": { "title": 1, "comments": 1 }       // Project relevant fields
    }
])
```

**Explanation**:
- Matches movies directed by Christopher Nolan.
- Joins with `comments` to get all related comments.

---

### Notes
- The `$lookup` stage can join only two collections at a time. For more complex joins, chain multiple `$lookup` stages.
- Ensure indexes exist on `localField` and `foreignField` to optimize performance.
- Use `$unwind` when dealing with nested arrays created by `$lookup`.

Let me know if you'd like to explore more specific examples!


The **general pattern for `$lookup`** in MongoDB is as follows:

---

### **Basic Structure of `$lookup`**
```javascript
{
    $lookup: {
        from: <foreign_collection>,       // The collection to join
        localField: <field_in_current>,   // The field from the current collection
        foreignField: <field_in_foreign>, // The field from the foreign collection
        as: <output_array_field>          // The name of the resulting array field
    }
}
```

### **Key Components**
1. **`from`**: The name of the foreign collection you want to join.
2. **`localField`**: The field in the current collection that serves as the join key.
3. **`foreignField`**: The field in the foreign collection that serves as the join key.
4. **`as`**: The name of the output array where the joined documents will be stored.

---

### **Example Patterns**

#### **1. One-to-Many Join**
If each document in the current collection can have multiple related documents in the foreign collection:
```javascript
{
    $lookup: {
        from: "foreign_collection",
        localField: "_id",
        foreignField: "current_collection_id",
        as: "related_documents"
    }
}
```

- Each document in the current collection will have an array `related_documents` containing all matching documents from the foreign collection.

---

#### **2. One-to-One Join**
If each document in the current collection can match exactly one document in the foreign collection:
```javascript
{
    $lookup: {
        from: "foreign_collection",
        localField: "_id",
        foreignField: "related_id",
        as: "single_document"
    }
}
```

- The resulting array in `as` will usually have one document, but it will still be an array unless further processed with `$unwind`.

---

#### **3. Adding Conditions with `$match` After `$lookup`**
You can filter the results of a `$lookup` using `$match`:
```javascript
[
    {
        $lookup: {
            from: "foreign_collection",
            localField: "field_in_current",
            foreignField: "field_in_foreign",
            as: "joined_data"
        }
    },
    {
        $match: { "joined_data.some_field": { $exists: true } }
    }
]
```

---

#### **4. Combine `$lookup` with `$unwind`**
If you need each joined document as a separate result (not in an array):
```javascript
[
    {
        $lookup: {
            from: "foreign_collection",
            localField: "field_in_current",
            foreignField: "field_in_foreign",
            as: "joined_data"
        }
    },
    {
        $unwind: "$joined_data"  // Flattens the joined array into individual documents
    }
]
```

---

#### **5. Using `$lookup` in Nested Joins**
You can chain `$lookup` stages to join multiple collections:
```javascript
[
    {
        $lookup: {
            from: "second_collection",
            localField: "field_in_first",
            foreignField: "field_in_second",
            as: "first_join"
        }
    },
    {
        $lookup: {
            from: "third_collection",
            localField: "first_join.field_in_second",
            foreignField: "field_in_third",
            as: "second_join"
        }
    }
]
```

---

### **Example Use Cases**

#### **Movies and Comments**
Link movies to their comments:
```javascript
{
    $lookup: {
        from: "comments",
        localField: "_id",
        foreignField: "movie_id",
        as: "comments"
    }
}
```

#### **Comments and Users**
Link comments to the users who made them:
```javascript
{
    $lookup: {
        from: "users",
        localField: "email",
        foreignField: "email",
        as: "user_details"
    }
}
```

---

### **Common Patterns for `$lookup`**

1. **One-to-Many Relationships**:
   - Use `$lookup` to join and add related documents as arrays.
   - Apply `$unwind` if necessary to process individual matches.

2. **Filtering Results After Join**:
   - Use `$match` to refine the results based on the joined data.

3. **Combining with `$project`**:
   - Use `$project` to include only the necessary fields from both collections.

4. **Handling Multiple Levels**:
   - Use nested `$lookup` stages to join across more than two collections.

5. **Optimizing with Indexes**:
   - Ensure `localField` and `foreignField` are indexed to improve performance.

---

### General Example
Suppose you want to join movies with comments and only include movies with more than 5 comments:
```javascript
db.movies.aggregate([
    {
        $lookup: {
            from: "comments",
            localField: "_id",
            foreignField: "movie_id",
            as: "movie_comments"
        }
    },
    {
        $match: { "movie_comments.5": { $exists: true } }  // Movies with at least 6 comments
    },
    {
        $project: { "title": 1, "movie_comments": 1 }  // Include only necessary fields
    }
])
```

This pattern illustrates how `$lookup` is combined with `$match` and `$project` for practical queries.