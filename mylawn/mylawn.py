from wunderground import get_weather_data


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
