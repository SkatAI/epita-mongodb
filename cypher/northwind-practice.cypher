// - Find all products more expensive than $50

MATCH (p:Product)
WHERE p.unitPrice > 50
RETURN p.productName, p.unitPrice

// which products are seafood, return product name and price
// Product PART_OF Category

MATCH (p:Product)-[:PART_OF]->(c:Category)
WHERE c.categoryName = 'Seafood'
RETURN p.productName, p.unitPrice

// return the path to see the graph

MATCH path=(:Product)-[:PART_OF]->(c:Category)
WHERE c.categoryName = 'Seafood'
RETURN path;

// Who supplies seafood product
// chain Suppliers with :SUPPLIES and Products
// Supplier SUPPLIES Product PART_OF Category

MATCH (s:Supplier)-[:SUPPLIES]->(p:Product)-[:PART_OF]->(c:Category)
WHERE c.categoryName = 'Seafood'
RETURN p.productName, p.unitPrice, s.companyName, s.country

// graph version

MATCH path=(s:Supplier)-[:SUPPLIES]->(p:Product)-[:PART_OF]->(c:Category)
WHERE c.categoryName = 'Seafood'
RETURN path

// also show the orders

MATCH path=(s:Supplier)-[:SUPPLIES]->(p:Product)-[:PART_OF]->(c:Category),
(o:Order)-[: ORDERS ]->(p)
WHERE p.unitPrice > 200
RETURN path

// that does not show the orders
// that does
// use : with path, p to create a new `layer`
MATCH path=(s:Supplier)-[:SUPPLIES]->(p:Product)-[:PART_OF]->(c:Category)
WHERE p.unitPrice > 50
WITH path, p
MATCH orderPath=(o:Order)-[: ORDERS ]->(p)
RETURN path, orderPath

// Which categories have the most expensive products?

MATCH (p:Product)-[:PART_OF]->(c:Category)
RETURN c.categoryName, max(p.unitPrice) AS maxPrice
 ORDER BY maxPrice DESC

// Find all orders shipped to London
MATCH (o:Order)
WHERE o.shipCity = 'London'
RETURN o.orderID, o.shipDate

// map all the products shipped to London

MATCH (o:Order)-[:ORDERS]->(p:Product)
WHERE o.shipCity = 'London'
RETURN o.orderID, o.shipDate, p.productName, p.unitPrice

// Who are our top 5 customers by number of orders?
// Customer :PURCHASED Order
// use count(o) as orderCount

MATCH (c:Customer)-[:PURCHASED]->(o:Order)
RETURN c.companyName, count(o) AS orderCount
 ORDER BY orderCount DESC
LIMIT 5

// Which products have never been ordered?
// Order :CONTAINS Product
// NOT EXISTS( (p) <-[:CONTAINS]-(:Order)   )

MATCH (p:Product)
WHERE NOT EXISTS( (p)<-[: CONTAINS ]-(:Order) )
RETURN p.productName

// return the product category as PATH

MATCH path=(p:Product)-[:PART_OF]->(c:Category)
WHERE NOT EXISTS( (p)<-[: CONTAINS ]-(:Order) )
RETURN path

// return the product category as PATH and also suppliers

MATCH path=(s:Supplier)-[:SUPPLIES]->(p:Product)-[:PART_OF]->(c:Category)
WHERE NOT EXISTS((p)<-[: CONTAINS ]-(:Order))
RETURN path

// Find all orders shipped by Speedy Express
//  a shipper SHIPPED an order

MATCH (s:Shipper)-[:SHIPPED]->(o:Order)
WHERE s.companyName = 'Speedy Express'
RETURN o.orderID

//  Which suppliers are in the same city as employees?
// Supplier city and Employee city

MATCH (s:Supplier), (e:Employee)
WHERE s.city = e.city
RETURN s.companyName, e.lastName, s.city

// Find products that need reordering (units in stock below reorder level)

MATCH (p:Product)
WHERE p.unitsInStock < p.reorderLevel
RETURN p.productName, p.unitsInStock, p.reorderLevel

// Find all employees who report to Andrew Fuller

MATCH (e:Employee)-[:REPORTS_TO]->(m:Employee { lastName: 'Fuller' })
RETURN e.firstName, e.lastName

//  using property filters on the node directly
//  inseatd of using a where clause you can filter the node

MATCH (o:Order)-[:ORDERS]->(p:Product)
WHERE o.shipCity = 'London'
RETURN o.orderID, o.shipDate, p.productName, p.unitPrice

MATCH (o:Order { shipCity : 'London' })-[:ORDERS]->(p:Product)
RETURN o.orderID, o.shipDate, p.productName, p.unitPrice

// or path

MATCH path=(o:Order { shipCity : 'London' })-[:ORDERS]->(p:Product)
RETURN path

// which product categories each supplier provides.
// note anonymous middle node since we don't need it in the results
// (s:Supplier)-->(:Product)-->(c:Category)
// The collect() function: Aggregates values into a list
// Returns an array of unique category names for each supplier

MATCH (s:Supplier)-->(:Product)-->(c:Category)
RETURN s.companyName AS company, collect( DISTINCT c.categoryName) AS categories

//  let's create new relatinos hips

// `FREQUENTLY_BOUGHT_WITH`: as in belong to the same order

MATCH (p1:product)<-[:ORDERS]-(Order)-[:ORDERS]->(p2:Product)
WHERE p1 < p2
WITH p1, p2, count(*) AS frequency
WHERE frequency > 10
MERGE (p1)-r:FREQUENTLY_BOUGHT_WITH-(p2)
 SET r.weight= frequency

// SUPPLIES_PRIMARILY: link supplier with the main categories supplied (via product)
// supplier supplies product in_category category

MATCH (s:Supplier)-[:SUPPLIES]->(p:product)-[:IN_CATEGORY] -> (c:Category)
WITH s, c, count(*) AS count
WHERE count > 3
MERGE (s)-r:SUPPLIES_PRIMARILY->(c)
 SET r.weight = count

MATCH (p1:Product)<-[:ORDERS]-(:Order)-[:ORDERS]->(p2:Product)
WHERE p1 < p2
WITH p1, p2, count(*) AS frequency
WHERE frequency > 10
MERGE (p1)-[r:FREQUENTLY_BOUGHT_WITH]-(p2)
 SET r.weight = frequency

// 2. `SUPPLIES_PRIMARILY`:
```cypher
MATCH (s:Supplier)-[:SUPPLIES]->(p:Product)-[:IN_CATEGORY]->(c:Category)
WITH s, c, count(*) AS count
WHERE count >= 3
MERGE (s)-[r:SUPPLIES_PRIMARILY]->(c)
 SET r.productCount = count
```

3. `SHIPS_TO_REGION`:
```cypher
MATCH (e:Employee)-[:PROCESSED]->(:Order)-[:SHIPPED_TO]->(c:Customer)
WITH e, c.region AS region, count(*) AS shipments
WHERE shipments > 5
MERGE (e)-[r:SHIPS_TO_REGION]->(region)
 SET r.shipmentCount = shipments
```

Want to explore any of these patterns IN detail?

1. Employee to Employee (worked together):
```cypher
MATCH (e1:Employee)-[:PROCESSED]->(:Order)<-[:PROCESSED]-(e2:Employee)
WHERE e1 < e2
WITH e1, e2, count(*) AS collaborations
WHERE collaborations > 5
MERGE (e1)-[r:WORKED_WITH]->(e2)
 SET r.orderCount = collaborations
```

2. Product to Product (shipped together):
```cypher
MATCH (p1:Product)<-[: CONTAINS ]-(:OrderDetail)-[:PART_OF]->(o:Order)<-[:PART_OF]-(:OrderDetail)-[: CONTAINS ]->(p2:Product)
WHERE p1 < p2
WITH p1, p2, count(*) AS coShipped
WHERE coShipped > 3
MERGE (p1)-[r:SHIPPED_WITH]->(p2)
 SET r.frequency = coShipped
```

3. Supplier to Supplier (shared categories):
```cypher
MATCH (s1:Supplier)-[:SUPPLIES]->(:Product)-[:IN_CATEGORY]->(c:Category)<-[:IN_CATEGORY]-(:Product)<-[:SUPPLIES]-(s2:Supplier)
WHERE s1 < s2
WITH s1, s2, count( DISTINCT c) AS sharedCategories
WHERE sharedCategories >= 2
MERGE (s1)-[r:SHARES_CATEGORIES]->(s2)
 SET r.count = sharedCategories
```
