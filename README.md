[![Build Status](https://travis-ci.org/jsurls/mylawn.svg?branch=master)](https://travis-ci.org/jsurls/mylawn)
[![Coverage Status](https://coveralls.io/repos/github/jsurls/mylawn/badge.svg?branch=master)](https://coveralls.io/github/jsurls/mylawn?branch=master)

## Developer Setup
```
# Install deps
pip install -r requirements-dev.txt
```

## Background
The seasonal of 100% is set to 1.5" of watering.

The following is assumed rate:
Rotor:    .5" per 60 minutes
Fan  :    .5" per 20 minutes

At 1.5" of watering it takes 10 hours to cycle through the yard (assuming no watering of the beds).

## Running
```
# Start AWS Infrastructure
localstack start

# Start Mock Wunderground Resource
docker-compose up

# Run from scripts dir
cd scripts

# Init database
python dynamo_create.py

# "Ask MyLawn how much water do I need?"
python run-alexa.py --file sample/get_water_guide.json

# "Set my zip code"
python run-alexa.py --file sample/set_station_from_zip.json

# "Ask again"
python run-alexa.py --file sample/get_water_guide.json
```

## Building
```
pyb
```
