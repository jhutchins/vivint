# Vivint Homework Project

The solution to the vivint homework problem for Jeff Hutchins.


## Running

The application can be run either as python vivint or by installing the
project with python setup.py install and using the provided vivint script.

By default the application will run on port 8080 with a default logging
verbosity of info. These options can be changed with the --port and --log
flags. For more info run the application with the --help flag.


## API Overview

All responses are wrapped in a JSON object under the key 'result'. This is so
the API might be more easily extended in the future without introducing
breaking changes to the API.


### Models

A thermostat object has the follow structure


|   attribute    |       value       | access |
|:--------------:|:-----------------:|:------:|
| name           | string            | r/w    |
| operating-mode | cool / heat / off | r/w    |
| cool-setpoint  | int; 30-100       | r/w    |
| heat-setpoint  | int; 30-100       | r/w    |
| fan-mode       | auto / on         | r/w    |
| current-temp   | int               | r/o    |
| id             | int               | r/o    |



## Endpoints

### GET /thermostats/

Return all the known information about all known thermostats.

Request:

```
GET /thermostats/ HTTP/1.1
Host: localhost:8080
User-Agent: curl/7.51.0
Accept: */*
```

Response (body formatted for readability):

```
HTTP/1.1 200 OK
Content-Type: application/json
Transfer-Encoding: chunked
Date: Sat, 15 Apr 2017 03:01:06 GMT
Server: localhost

{ "result": [
  {
    "name": "Upstairs Thermostat",
    "operating-mode": "heat",
    "cool-setpoint": 75,
    "heat-setpoint": 65,
    "fan-mode": "auto",
    "current-temp": 71,
    "id": 100
  },
  {
    "name": "Downstairs Thermostat",
    "operating-mode": "heat",
    "cool-setpoint": 75,
    "heat-setpoint": 65,
    "fan-mode": "auto",
    "current-temp": 69,
    "id": 101
  }
]}
```


### GET /thermostats/<id>/

Return all know information for a specified thermostat. Return 404 if
not found.


Request:

```
GET /thermostats/100/ HTTP/1.1
Host: localhost:8080
User-Agent: curl/7.51.0
Accept: */*
```

Response (body formatted for readability):

```
HTTP/1.1 200 OK
Content-Type: application/json
Transfer-Encoding: chunked
Date: Sat, 15 Apr 2017 03:01:06 GMT
Server: localhost

{ "result": {
    "name": "Upstairs Thermostat",
    "operating-mode": "heat",
    "cool-setpoint": 75,
    "heat-setpoint": 65,
    "fan-mode": "auto",
    "current-temp": 71,
    "id": 100
}}
```


### PATCH /thermostats/<id>/

Update a group of attributes for a given thermostat. The payload must be a
JSON object of attributes and values. The result will include the attributes
and the result on the update for each. A 404 will be returned if the
thermostat indicated is unknown.


Request (body formatted for readability):

```
PATCH /thermostats/100/ HTTP/1.1
Host: localhost:8080
User-Agent: curl/7.51.0
Content-Type: application/json
Content-Length: 78
Accept: */*

{
  'name': 'New Name',
  'id': 5,
  'cool-setpoint': 'warm',
  'location': 'bathroom'
}
```


Response (body formatted for readability):

```
HTTP/1.1 200 OK
Content-Type: application/json
Transfer-Encoding: chunked
Date: Sat, 15 Apr 2017 03:01:06 GMT
Server: localhost

{'result': {
    'name': 'ok',
    'id': 'value is readonly',
    'cool-setpoint': 'value must be an integer',
    'location': 'unknown attribute'
}}
```


 ### GET /thermostats/<id>/<name>

Get the value of the named attribute for the identified thermostat. The result
will be a JSON encoded value (number of string). Inability to locate either the
thermostat or the named attribute will result in a 404.


Request:

```
GET /thermostats/100/cool-setpoint HTTP/1.1
Host: localhost:8080
User-Agent: curl/7.51.0
Accept: */*
```

Response (body formatted for readability):

```
HTTP/1.1 200 OK
Content-Type: application/json
Transfer-Encoding: chunked
Date: Sat, 15 Apr 2017 03:01:06 GMT
Server: localhost

75
```


### PUT /thermostats/<id>/<name>

Set the named attribute to the given value for the identified thermostat. The
value must be a JSON encode value (string or integer) of the appropriate type
and value for the named attribute. Success will result in a 204, failure to
find the attribute or thermostat in a 404 and 403 for attempts to write
read-only attributes (id & current-temp).


Request:

```
PUT /thermostats/100/fan-mode HTTP/1.1
Host: localhost:8080
User-Agent: curl/7.51.0
Content-Type: application/json
Content-Length: 4
Accept: */*

"on"
```


Response (body formatted for readability):

```
HTTP/1.1 204 No Content
Date: Sat, 15 Apr 2017 03:01:06 GMT
Server: localhost
```
