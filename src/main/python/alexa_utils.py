ALEXA_PAUSE = '<break time="1ms"/>'
ALEXA_START = '<speak>'
ALEXA_FINISH = '</speak>'


def end_session():
    """ Returns a basic message with no sentences, ending the session. """
    return basic_message()


def basic_message(sentences=None, should_end_session=True):
    """ Creates a basic message alexa will say. """
    verbiage = alexify(sentences)
    speechlet = build_speechlet_response(verbiage, should_end_session)
    return build_response({}, speechlet)


def alexify(statements):
    """
    Wraps statements into an Alexa Speech envelope
    :return: alexa speech envelope
    """
    if statements is None:
        return None

    return "".join([ALEXA_START,
                    ALEXA_PAUSE.join(statements),
                    ALEXA_FINISH])


def build_speechlet_response(output, should_end_session):
    if output is None:
        return {"shouldEndSession": should_end_session}

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
