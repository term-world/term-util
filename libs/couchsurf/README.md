# `couchsurf`: world communication with `couchdb`

The `couchsurf` library enables two-way communication with an Apache `CouchDB` server provided by environment variables.

## Using `couchsurf`

### 

Couchsurf requires creating a `Connection` object, which ferries communication between the local and remote servers:

```python
from couchsurf import Connection

# Connect to "marketplace" DB
conn = Connection("marketplace")
```

This enables `request`s to the server, such as `PUT`, and `POST`.

#### `PUT` requests

`PUT` requests add records to the database. In order to do this, request a new record ID _prior_ to making your
`PUT request:

```python
id = conn.request.get_new_id()
conn.request.put(
    doc_id = id,
    doc = {"field1": "value", "field2": "value"}
)
```

#### `POST` requests

`POST` requests are currently limited to querying a database for matching records. To query, provide a keyword argument
for each parameter to query and an accompanying dictionary featuring the operator and query argument (i.e. criteria)
to match.

Currently, the library supports the following operators:

|Operator |Expression |
|:--------|:----------|
|Less than|`LESS THAN`|
|Greater than|`GREATER THAN`|
|Equal to |`EQUALS`|
|Like |`LIKE`|

```python

# Querying (aka POSTing)
libraries = conn.request.query(
    type={"op": "EQUALS", "arg": "library"}
)
```
