import datastore
import re
import logging
from mylawn import get_water_info
from alexa_utils import basic_message, alexify, build_speechlet_response, build_response

# Setup basic logging
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def get_weather_data(session):
    """ Handles intents for 'GetWaterGuide """

    # Get the user id and session attributes
    user_id = session["user"]["userId"]
    session_attributes = session.get("attributes", {})

    # Lookup wunderground station by user_id
    logger.info("Looking up station for %s", user_id)
    wundergound = get_station_for_user(user_id)

    # Setup user configuration if it doesn't exist
    if wundergound is None:
        session_attributes["get_weather_data"] = True
        return basic_message(["I don't know where we are.", "What is your zip code?"], False)

    # Return the weather data
    logger.info("Using station %s for user %s", wundergound, user_id)
    verbiage = alexify(get_water_info(wundergound))
    speechlet = build_speechlet_response(verbiage, True)
    return build_response(session_attributes, speechlet)


def set_station_from_zip(intent, session):
    """ Handles intents for 'SetStationFromZip' """
    try:
        # Get user id and supplied zipcode
        user_id = session["user"]["userId"]
        zipcode = intent["slots"]["zipcode"].get('value', None)

        # Alexa could not decode the input
        if zipcode is None or zipcode == "?":
            messages = ["I am having difficulty understanding your zipcode.",
                        "Try saying your five digit zipcode again."]
            return basic_message(messages, False)

        # The zipcode provided was not 5 digits
        if len(str(zipcode)) < 5:
            messages = ["The zip code <say-as interpret-as=\"spell-out\">%s</say-as>"
                        " was not five digits in length" % zipcode,
                        "Try saying your five digit zipcode again."]
            return basic_message(messages, False)

        set_station_for_user(user_id, zipcode)

        zip_response = "I'll remember <say-as interpret-as=\"spell-out\">%s</say-as> as your default zipcode" % zipcode
        return basic_message([zip_response])
    except ValueError:
        return basic_message(["I was unable to lookup that zipcode"])


# --------------- Helper Methods -----------------------------------------------

def get_station_for_user(user_id):
    """ Finds the saved wunderground station by user id """
    # Fetch the user
    user = datastore.get_user(user_id)

    # Return None for station_id if user does not exist
    if user is None:
        return None

    # Return None if station_id is not set
    station = user.get('station_id', None)

    if station is None:
        return None

    # Patch to force Stations to Zipcode
    # TODO: Remove this later
    if not re.match(r'\d{5}$', station):
        return None

    return station


def set_station_for_user(user_id, station_id):
    """ Sets the station id for this user """
    # Fetch the user
    user = datastore.get_user(user_id)

    # Create user if one doesn't exist
    if user is None:
        user = {
            'id': user_id,
        }

    # Set the station id
    user['station_id'] = station_id

    # Save user
    datastore.put_user(user)
