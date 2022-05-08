# GCS BackEnd Documentation

### Objective:
-
-

### Prerequisites:
- Python 3.7 or greater installed
- Install pip(package installer for python)
  - [pip documentation click here](https://pip.pypa.io/en/stable/installation/)

### How To Run
1. Install `virtualenv`:
```
$ pip install virtualenv
```

2. Open a terminal in the project root directory and run:
```
$ virtualenv env
```

3. Run the command:
```
$ .\env\Scripts\activate (Powershell)
or
$ source env/Scripts/activate (for GitBash)
```

4. Install the dependencies:
```
$ (env) pip install -r requirements.txt
```

5. Finally start the server:
```
$ (env) python app.py
```

## API Endpoints:
_TO BE UPDATE_


### _Example Geofence format (for MAC, MEA, and ERU)_
```
{
    "geofence": [
        {
          "coordinates": [
            {
              "lat": 0.0,
              "lng": 0.0
            },
            {
              "lat": 0.0,
              "lng": 0.0
            },
            {
              "lat": 0.0,
              "lng": 0.0
            },
          ],
          "keep_in": true
        },
        {
          "coordinates": [
            {
              "lat": 0.0,
              "lng": 0.0
            },
            {
              "lat": 0.0,
              "lng": 0.0
            },
            {
              "lat": 0.0,
              "lng": 0.0
            },
          ],
          "keep_in": false
        }
      ]
}
NOTE: Geofence is an array of objects. Each object represents a single polygon. A polygon is composed of the boolean 'Keep_in' and an array that can contain any number of coordinates. Also keeping track of circle inputs for repopulating GUI with previous inputs.
```

### _Example Search Area format_
```
{
    "search_area": [
        {
          "lng": 0.0,
          "lat": 0.0
        },
        {
          "lng": 0.0,
          "lat": 0.0
        },
        {
          "lng": 0.0,
          "lat": 0.0
        }
      ]
}
NOTE: Search Area is an array of objects that describe an area made up of longitudes and latitudes pairs
```

### _Example Home Coordinates format_
```
{
    "home_coordinates": {
        "1": {
          "vehicle": "MAC",
          "lat": 33.93368449228065,
          "lng": -117.63028265435334
        },
        "2": {
          "vehicle": "MEA",
          "lat": 33.934454472545525,
          "lng": -117.63246060807343
        },
        "3": {
          "vehicle": "ERU",
          "lat": 33.93368449228065,
          "lng": -117.63077618081208
        }
      },
}
NOTE: Each vehicle has its own home coordinates
```

### _Example Drop Coordinates format_
```
{
  "drop_coordinates":
    {
      "lat": 33.93436545784193,
      "lng": -117.6308888335907
    }
}
Note: Drop coordinates are for MAC
```

### _Example Evacuation Coordinates format_
```
{
  "evacuation_coordinates":
  {
    "lat": 33.934071708659815,
    "lng": -117.63107658822175
  }
}
Note: Evacuation coordinates are for MEA and ERU
```
