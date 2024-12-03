# Neo4j on EU

Data Model Design
First, let's identify our main entities and relationships:

Nodes:

MEPs (Members of European Parliament)
Debates (Sessions)
Political Parties


Relationships:

MEPs BELONGS_TO Party
MEPs SPEAKS_IN Debate
MEPs FOLLOWS Other_MEP (if we want to track who speaks after whom)