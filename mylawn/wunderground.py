import datetime
import json
import re
import urllib2

import requests
import datastore

from config.settings import WUNDERGROUND_KEY

from config.settings import WUNDERGROUND_HOST


def get_weather_data(weather_station):
    """
    Queries a nearby weather underground station for temp data and rain data
    :param weather_station: weather underground weather station id
    :return: (average_temp, total_rain)
    """
    now = datetime.datetime.now()
    then = now - datetime.timedelta(days=7)

    endpoint = WUNDERGROUND_HOST + '/weatherstation/WXDailyHistory.asp?graphspan=custom&format=1'
    query_weather_station = ("ID=%s" % weather_station)
    query_date_start = ("day=%s&month=%s&year=%s" % (then.day, then.month, then.year))
    query_date_end = ("dayend=%s&monthend=%s&yearend=%s" % (now.day, now.month, now.year))

    weather_url = ("%s&%s&%s&%s" % (endpoint, query_weather_station, query_date_start, query_date_end))

    # print weather_data_url
    html_data = requests.get(weather_url).text

    weather_data = filter(lambda x: not re.match(r'^\s*$', x) and not re.match(r'^.*<br>.*$', x),
                          html_data.splitlines())

    avg_temp = avg(map(lambda x: float(x.split(",")[1]), weather_data))
    total_rain = sum(map(lambda x: float(x.split(",")[-1]), weather_data))

    return avg_temp, total_rain


def avg(sequence):
    return reduce(lambda x, y: x + y, sequence) / len(sequence)


def get_station_by_zipcode(zipcode):
    """
    Gets the nearest pws station id to this zipcode
    :param zipcode:
    :return: station_id
    """
    try:
        # Check locally first
        geolookup = datastore.get_geolookup(zipcode)

        # Call wunderground and store it for future calls
        if geolookup is None:
            station_id = wunderground_geo_locate(zipcode)
            if station_id is None:
                return None
            else:
                geolookup = {'id': str(zipcode), 'station_id': station_id}
                datastore.put_geolookup(geolookup)

        return geolookup.get('station_id')
    except Exception as error:
        print("Unexpected exception while fetching station for zipcode: " + zipcode, error)
        return None


def wunderground_geo_locate(zipcode):
    """
    Wunderground API Helper to call geolookup with zipcode
    :param zipcode:
    :return: first station_id
    """
    endpoint = WUNDERGROUND_HOST + '/api/' + WUNDERGROUND_KEY + '/geolookup/q/' + zipcode + '.json'
    print("Endpoint: " + endpoint)
    stream = urllib2.urlopen(endpoint)
    response = json.loads(stream.read())
    return response['location']['nearby_weather_stations']['pws']['station'][0]['id']
