# Introduction
This project aims to design and develop a simple device that will allow a user to monitor a room’s sound level and any motion occurring inside. The device will send all the data it gathers to a remote API, where it will then be possible to visualize it in various helpful ways. 

# Target Audience
This device is aimed towards people looking to monitor movements and sound in a certain space they own. This could be for security purposes, or any other purpose (similar systems have been used for sleep pattern research, etc.). The goal is to allow users to know when activity occurred in a certain space. 

# Hardware Design: 

## Sensors Used: 
Sound sensor 
PIR motion sensor 
## Hardware Schematics: 
![IOT2project_bb_no_led](https://user-images.githubusercontent.com/77691927/209218507-16f9612f-4da7-477c-8577-32a67c8390bc.png)

## Sensor Data Sampling and Specification: 
The sound sensor will measure sounds in a decibel value. It also contains a digital output that returns 1 if the sound is above a certain threshold. 
The motion sensor detects the presence of an infrared signature in front of it, outputting 1 if it does detect one. 

# MongoDB Schema Design
The MongoDB database will contain two collections, one with the readings of the sound sensor and one with the reading of the motion sensor. 

The sound sensor readings will be sent to the database when the average of the readings over the last minute. If the sound readings are above 650, it will mark the minute as having had sound. Otherwise, it will not.

Meanwhile, the motion sensor data will be the count of seconds over a minute where motion was detected. If more than 40 seconds included movements, the minute will be marked as having had movements.

# API Endpoints:
## Get Sound Levels  
Get the individual sound levels 

`/api/sound`

Query parameters: 
- `average`: bool – return individual readings or daily averages (FALSE by default) 
- `year`: int – specify a year 
- `month`: int – specify a month (generally 1-12) 
- `day`: int – specify a day in a month (generally 1-31) 
Sample Response:  
```[ 
  { 
    "date": { 
      "day": 3, 
      "hour": 16, 
      "millisecond": 0, 
      "minute": 35, 
      "month": 12, 
      "second": 26, 
      "year": 2022 
    }, 
    "value": 1929 
  } 
]
```


With `?average=true`: 
```
[ 
  { 
    "_id": { 
      "date": { 
        "day": 6, 
        "month": 12, 
        "year": 2022 
      } 
    }, 
    "average": 689.5 
  } 
]
```

## Get Motion Levels

`/api/motion`

Query parameters: 
- `count`: bool – return individual readings or daily count(FALSE by default) 
- `year`: int – specify a year 
- `month`: int – specify a month (generally 1-12) 
- `day`: int – specify a day in a month (generally 1-31) 

Sample Response:  
```
[ 
  { 
    "date": { 
      "day": 3, 
      "hour": 16, 
      "millisecond": 0, 
      "minute": 35, 
      "month": 12, 
      "second": 26, 
      "year": 2022 
    }, 
    "value": 20 
  } 
] 
```

With `?count=true`: 

```
[ 
  { 
    "_id": { 
      "date": { 
        "day": 6, 
        "month": 12, 
        "year": 2022 
      } 
    }, 
    "count": 120 
  } 
]
```

## Create Sound Entry 

Creates a sound entry in the database. 

`/api/sound`

JSON Request structure: 

```
{ 
    “value”: (int) 
    “sensorId”: (str) 
} 
```

Sample Response: 

```
{ 
    "_id": "638ff3767d3983ac62044034", 
    "sensorId": "TestSound", 
    "soundHeard": true, 
    "timestamp": "Tue, 06 Dec 2022 20:59:18 GMT", 
    "value": 2000 
} 
```

## Create Motion Entry 

Creates a motion entry in the database. 

`/api/motion`

JSON Request structure: 

```
{ 
    “value”: (int) 
    “sensorId”: (str) 
}	 
```

Sample Response:  

```
{ 
    "_id": "638ff2ea7d3983ac62044033", 
    "motionSeen": true, 
    "sensorId": "MotionTest", 
    "timestamp": "Tue, 06 Dec 2022 20:56:58 GMT", 
    "value": 40 
} 
```
