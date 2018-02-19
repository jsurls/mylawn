#!/bin/env python
from __future__ import print_function

import os

from session_utils import get_application_id
from alexa_intents import on_stop, on_help, on_cancel
from mylawn_intents import get_weather_data, set_station_from_zip
from alexa_utils import basic_message, end_session
import json


# --------------- Lambda Handler -----------------------------------------------


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("AUDIT: event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    app_id = get_application_id(event)

    """
    Verify your skill's application ID to prevent someone else from
    configuring a skill that sends requests to this function.
    """
    if app_id != os.getenv('app_id', app_id):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    response = None
    if event['request']['type'] == "LaunchRequest":
        response = on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        response = on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        response = on_session_ended(event['request'], event['session'])

    print("Response: " + json.dumps(response))
    if response['response']['shouldEndSession']:
        print("session_end_response")

    return response


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("EVENT: start_session --> requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want """

    print("EVENT: launch --> requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return basic_message(["Hello.", "I am your lawn and I am here to help.",
                          "Feel free to ask how much should I water.",
                          "What would you like to do?"], False)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    print("EVENT: intent --> requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])

    print("User: " + session["user"]["userId"])

    print("Session: " + json.dumps(session))
    print("Session Attributes: " + str(session.get("attributes", {})))

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print("Intent Request: " + json.dumps(intent_request))
    print("Intent Name: " + intent_name)

    # Handle default Amazon intents
    if intent_name == "AMAZON.HelpIntent":
        return on_help(intent, session)
    elif intent_name == "AMAZON.StopIntent":
        return on_stop(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        return on_cancel(intent, session)

    # Dispatch to your skill's intent handlers
    if intent_name == "SetStationFromZip":
        return set_station_from_zip(intent, session)
    elif intent_name == "GetWaterGuide":
        return get_weather_data(session)

    # Default intent
    print("UNKNOWN INTENT: " + intent_name)
    return on_help(intent, session)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("EVENT: end_session --> requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    return end_session()
