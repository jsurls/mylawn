#!/bin/env python
from __future__ import print_function

import datastore
from config.settings import ALEXA_APP_ID
from mylawn import get_water_info

ALEXA_PAUSE = '<break time="1ms"/>'
ALEXA_START = '<speak>'
ALEXA_FINISH = '</speak>'


# --------------- Lambda Handler -----------------------------------------------


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Verify your skill's application ID to prevent someone else from
    configuring a skill that sends requests to this function.
    """
    if event['session']['application']['applicationId'] != ALEXA_APP_ID:
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    # return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "SetStationFromZip":
        return set_station_from_zip(intent, session)

    # Default intent
    return get_weather_data(session)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Functions that control the skill's behavior ------------------

def get_weather_data(session):
    """ Gets weather data for the supplied user """

    # Get the user id and session attributes
    user_id = session["user"]["userId"]
    session_attributes = session.get("attributes", {})

    # print("event.request.type: ", request.get("type"))
    print("session.new: ", session.get("new"))
    print("event.session.userId: ", user_id)
    print("event.session.attributes: ", session_attributes)

    # Lookup wunderground station by user_id
    wundergound = get_station_for_user(user_id)

    # Setup user configuration if it doesn't exist
    if wundergound is None:
        session_attributes["get_weather_data"] = True
        return basic_message(["I don't know where we are.", "What is your zip code?"])

    # Return the weather data
    verbage = alexify(get_water_info(wundergound))
    speechlet = build_speechlet_response(verbage, True)
    return build_response(session_attributes, speechlet)


def find_station_by_zip(zipcode):
    """ Finds the nearest wundergound station by zipcode """
    # TODO: validate zipcode
    return 'KTXAUSTI905'


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


def set_station_from_zip(intent, session):
    try:
        # Get user id and supplied zipcode
        user_id = session["user"]["userId"]
        zipcode = intent['slots']['zipcode']['value']

        # Get the station id for this zipcode and save it for the user
        station_id = find_station_by_zip(zipcode)
        set_station_for_user(user_id, station_id)

        zip_response = "I'll remember <say-as interpret-as=\"spell-out\">%s</say-as> as your default zipcode" % zipcode
        return basic_message([zip_response])
    except ValueError:
        return basic_message(["I was unable to lookup that zipcode"])


# --------------- Helpers that build all of the responses ----------------------

def basic_message(sentences):
    """ Creates a basic message alexa will say, ending the session. """
    verbage = alexify(sentences)
    speechlet = build_speechlet_response(verbage, True)
    return build_response({}, speechlet)


def alexify(statements):
    """
    Wraps statements into an Alexa Speech envelope
    :return: alexa speech envelope
    """
    return "".join([ALEXA_START,
                    ALEXA_PAUSE.join(statements),
                    ALEXA_FINISH])


def build_speechlet_response(output, should_end_session):
    return {
        "outputSpeech": {
            "type": "SSML",
            "ssml": output
        },
        "shouldEndSession": should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
