# Neo4j

Graph elements

https://graphacademy.neo4j.com/courses/neo4j-fundamentals/1-graph-thinking/2-graph-elements/

Relationships are typically verbs.

We could use a relationship to represent a personal or professional connection (Person knows Person, Person married to Person), to state a fact (Person lives in Location, Person owns Car, Person rated Movie), or even to represent a hierarchy (Parent parent of Child, Software depends on Library).

Directed vs. undirected graphs
Michael and Sarah are married to each other

In an undirected graph, relationships are considered to be bi-directional or symmetric.

Weighted vs. unweighted graphs

More complex shortest path algorithms (for example, Dijkstra’s algorithm or A* search algorithm) take a weighting property on the relationship into account when calculating the shortest path. Say we have to send a package using an international courier, we may prefer to send the package by air so it arrives quickly, in which case the weighting we would take into account is the time it takes to get from one point to the next.