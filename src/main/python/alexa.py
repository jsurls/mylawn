import os
import json
import logging

from session_utils import get_application_id, get_user_id
from alexa_intents import on_stop, on_help, on_cancel
from mylawn_intents import get_weather_data, set_station_from_zip
from alexa_utils import basic_message, end_session


# Setup basic logging
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    logger.info('Event: %s', json.dumps(event))

    try:
        app_id = get_application_id(event)
        logger.info('Application id: %s', app_id)

        """
        Verify your skill's application ID to prevent someone else from
        configuring a skill that sends requests to this function.
        """
        if app_id != os.getenv('APP_ID', app_id):
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

        logger.info("Response: %s", json.dumps(response))
        if response['response']['shouldEndSession']:
            logger.info("Response indicates session will end")

        return response
    except Exception as e:
        logging.error('Failed to handle event', exc_info=e)
        return basic_message(["I am unable to get your lawn information right now.",
                              "Please try again later."], True)


def on_session_started(session_started_request, session):
    """ Called when the session starts """
    logger.info("New session")


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want """
    logger.info("Launch Request")

    # Dispatch to your skill's launch
    return basic_message(["Hello.", "I am your lawn and I am here to help.",
                          "Feel free to ask how much should I water.",
                          "What would you like to do?"], False)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    user_id = get_user_id(session)
    logger.info("Identified user: %s", user_id)

    # Determine intent of the User
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    logger.info("Intent Name: %s", intent_name)

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
    logger.warn("Unknown intent: %s", intent_name)
    return on_help(intent, session)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    logger.info("User ended session")
    return end_session()
