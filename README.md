# Micropy
A Microservice example written in Python with an eye-candy browser interface.

## Run
1. Create and activate a Virtualenv
1. pip install -r requirements.txt 
1. ./app.py

## Usage
Server Heartbeat:
```bash
curl "http://127.0.0.1:8000/"
```

Insert record:
```bash
curl -H "Content-Type: application/json" -X POST -d '{"action": 2, "timestamp": "2017-05-28T16:01:00.00219Z"}' http://127.0.0.1:8000/user/1/

```

Query:
```bash
curl "http://127.0.0.1:8000/user/1/?start=2017-05-28T12:01:00.00213Z&end=2017-05-28T17:03:00.00220Z"
```

## Persistence
This project uses Apache Cassandra to keep a record of all transactions.
This database is only used to persist data. 

Cassandra download instructions: http://cassandra.apache.org/download/
1. Create Keyspace
```sql
CREATE KEYSPACE micropy
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
AND DURABLE_WRITES = True;
```
2. Use Keyspace
```sql
USE micropy;
```

3. Create Table
```sql
CREATE TABLE actions (
  uid int,
  action int,
  timestamp varchar,
  PRIMARY KEY (uid, timestamp, action)
);
```
4. Query
```sql
SELECT * FROM actions;
```

## Improvements
1. Unit testing (requests + unittest)
2. Continuous Integration