import datetime
import json
import logging
import os

import requests

WUNDERGROUND_KEY = os.getenv('WUNDERGROUND_KEY')
WUNDERGROUND_HOST = os.getenv('WUNDERGROUND_HOST')

# Setup basic logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def get_weather_data(weather_station):
    """
    Queries a nearby weather underground station for temp data and rain data
    :param weather_station: weather underground weather station id
    :return: (average_temp, total_rain)
    """
    now = datetime.datetime.now()
    then = now - datetime.timedelta(days=7)

    query_date_start = ("%d%02d%02d" % (then.year, then.month, then.day))
    query_date_end = ("%d%02d%02d" % (now.year, now.month, now.day))

    api_key = '/api/%s' % WUNDERGROUND_KEY
    history_key = '/history_%s%s/lang:EN/units:english/bestfct:1/v:2.0' % (query_date_start, query_date_end)
    query = '/q/%s.json?showObs=0&ttl=120' % weather_station

    weather_url = ("%s%s%s%s" % (WUNDERGROUND_HOST, api_key, history_key, query))

    logger.info('Weather URL: %s', weather_url)
    response = requests.get(weather_url).text

    max_temp_avg = json.loads(response)['history']['summary']['max_temperature_avg']
    sum_precip = json.loads(response)['history']['summary']['precip_sum']

    return max_temp_avg, sum_precip
