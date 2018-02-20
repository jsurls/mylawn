import datastore
from mylawn import get_water_info
from wunderground import get_station_by_zipcode
from alexa_utils import basic_message, alexify, build_speechlet_response, build_response


def get_weather_data(session):
    """ Handles intents for 'GetWaterGuide """

    # Get the user id and session attributes
    user_id = session["user"]["userId"]
    session_attributes = session.get("attributes", {})

    # Lookup wunderground station by user_id
    wundergound = get_station_for_user(user_id)

    # Setup user configuration if it doesn't exist
    if wundergound is None:
        session_attributes["get_weather_data"] = True
        return basic_message(["I don't know where we are.", "What is your zip code?"], False)

    # Return the weather data
    verbage = alexify(get_water_info(wundergound))
    speechlet = build_speechlet_response(verbage, True)
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

        # Get the station id for this zipcode and save it for the user
        station_id = get_station_by_zipcode(zipcode)
        if station_id is None:
            message = "I was unable to find a station with the zipcode " \
                      "<say-as interpret-as=\"spell-out\">%s</say-as>" % zipcode
            return basic_message([message])

        set_station_for_user(user_id, station_id)

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
    return user.get('station_id', None)


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
