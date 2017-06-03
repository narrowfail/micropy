# micropy
A Microservice example written in Python.

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
