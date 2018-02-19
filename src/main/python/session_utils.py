

# Event Utils
def get_application_id(event):
    return event['session']['application']['applicationId']


def get_request_type(event):
    return event['request']['type']


def get_request(event):
    return event['request']


def get_session(event):
    return event['session']


def is_new_session(event):
    if event['session']['new']:
        return True
    return False


# Session Utils
def get_user_id(session):
    return session["user"]["userId"]


# Response Utils
def is_end_session(response):
    return response['response']['shouldEndSession']


# Intent Utils
def get_intent_name(intent):
    return intent['name']


def get_number_value(intent):
    return intent['slots']['number']['value']
