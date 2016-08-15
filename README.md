[![Build Status](https://travis-ci.org/jsurls/mylawn.svg?branch=master)](https://travis-ci.org/jsurls/mylawn)

## Developer Setup
```
# Install virtualenv and virtualenvwrapper
pip install virtualenv
pip install virtualenvwrapper 
```

## Background
The seasonal of 100% is set to 1.5" of watering.

The following is assumed rate:
Rotor:    .5" per 60 minutes
Fan  :    .5" per 20 minutes

At 1.5" of watering it takes 10 hours to cycle through the yard (assuming no watering of the beds).

## Running
```
# Start Docker Infrastructure
docker-compose up

# Init database
python scripts/dynamo_create.py

# "Ask MyLawn how much water do I need?"
python run-alexa.py --file sample/get_water_guide.json

# "Set my zip code"
python run-alexa.py --file sample/set_station_from_zip.json

# "Ask again"
python run-alexa.py --file sample/get_water_guide.json
```

## Building
```
build.sh
```
