#!/bin/env python
from __future__ import print_function

from alexa_utils import basic_message, end_session


def on_help(intent, session):
    """ Called when the user says 'help' """
    # Dispatch to your skill's launch
    return basic_message(["Hello.", "I am your lawn and I am here to help.",
                          "Ask me questions like.",
                          "How much water does my lawn need?",
                          "If you would like to me to repeat what I can do, just ask for help again.",
                          "What would you like to do?"], False)


def on_stop(intent, session):
    """ Called when the user says 'stop' """
    return end_session()


def on_cancel(intent, session):
    """ Called when the user says 'cancel' """
    return basic_message(None, False)
