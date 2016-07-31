#!/bin/env python
import datetime
import re
import requests


def get_water_info(weather_station):
    # Collect weather data
    (avg_temp, total_rain) = get_weather_data(weather_station)

    return [weather_message(avg_temp, total_rain),
            water_message(avg_temp, total_rain),
            mow_message(avg_temp)]


def weather_message(avg_temp, total_rain):
    """
    Return average high and amount of rain received for the past week
    :param avg_temp: average daytime high
    :param total_rain: total rain received
    :return: what the avg temp and total rain was for the past week
    """
    return "The avg high was %s degrees with %s inches of rain." % (round(avg_temp), total_rain)


def mow_message(avg_temp):
    """
    Return mowing height message
    :param avg_temp: average daytime high
    :return: mowing height message`
    """
    return "You should mow at the %s setting." % mow_guidance(avg_temp)


def water_message(avg_temp, total_rain):
    water_amount = water_guidance(avg_temp)
    water_needed = max(water_amount - total_rain, 0)

    if water_needed > 0:
        message_template = "You need %s inches to reach %s inches for the week.  <break time=\"2ms\"/> Water %.0f%%."
        return message_template % (water_needed, water_amount, water_needed / .015)
    else:
        return "You've exceeded %s inches for the week. Turn off sprinklers." % water_amount


def get_weather_data(weather_station):
    """
    Queries a nearby weather underground station for temp data and rain data
    :param weather_station: weather underground weather station id
    :return: (average_temp, total_rain)
    """
    now = datetime.datetime.now()
    then = now - datetime.timedelta(days=7)

    endpoint = "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?graphspan=custom&format=1"
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


def water_guidance(temp):
    """
    Return a float of how much water is needed
    based on temperature
    :param temp: average daytime high
    :return: water in inches needed
    """
    if temp >= 100:
        # return 1.75
        return 1.5
    elif temp >= 94:
        return 1.5
    elif temp >= 89:
        return 1.25
    elif temp >= 84:
        return 1.0
    elif temp >= 70:
        return 0.75
    else:
        return 0


def mow_guidance(temp):
    """
    Return mowing height
    :param temp: average daytime high
    :return: mowing height
    """
    if temp < 84:
        return "lowest"
    elif temp > 95:
        return "highest"
    else:
        return "regular"


def avg(sequence):
    return reduce(lambda x, y: x + y, sequence) / len(sequence)
