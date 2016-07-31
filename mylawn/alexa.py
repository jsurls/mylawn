#!/bin/env python
from __future__ import print_function
from mylawn import get_water_info

import json

ALEXA_PAUSE = '<break time="1ms"/>'
ALEXA_START = '<speak>'
ALEXA_FINISH = '</speak>'


# --------------- Lambda Handler -----------------------------------------------


def lambda_handler(event, context):
    # TODO: Remove hard coded wunderground station
    return json.dumps(build_response(build_speechlet_response(alexify(get_water_info('KTXCEDAR6')), True)))


# --------------- Helpers that build all of the responses ----------------------


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


def build_response(speechlet_response):
    return {
        "version": "1.0",
        "response": speechlet_response
    }
