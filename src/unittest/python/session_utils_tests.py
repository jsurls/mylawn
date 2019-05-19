from __future__ import absolute_import

import unittest

import helper
import session_utils


class SessionUtilsTest(unittest.TestCase):
    def test_get_application_id(self):
        event = helper.alexa_skills_request('get_water_guide.json')

        result = session_utils.get_application_id(event)

        self.assertEqual(result, 'amzn1.echo-sdk-ams.app.00000000-0000-0000-0000-000000000000')

    def test_get_request_type(self):
        event = helper.alexa_skills_request('get_water_guide.json')

        result = session_utils.get_request_type(event)

        self.assertEqual(result, 'IntentRequest')

    def test_get_request(self):
        event = helper.alexa_skills_request('get_water_guide.json')

        result = session_utils.get_request(event)

        self.assertIsNotNone(result)
        self.assertIsNotNone(result.get("type"))

    def test_get_session(self):
        event = helper.alexa_skills_request('get_water_guide.json')

        result = session_utils.get_session(event)

        # we should have a result
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.get("sessionId"))

    def test_is_new_session(self):
        event = {
            'session': {
                'new': True
            }
        }

        # Check new session
        result = session_utils.is_new_session(event)
        self.assertTrue(result)

        # Check old session
        event['session']['new'] = False
        result = session_utils.is_new_session(event)
        self.assertFalse(result)

    def test_get_user_id(self):
        expected = 'user_123'
        session = {
            'user': {
                'userId': expected
            }
        }

        result = session_utils.get_user_id(session)
        self.assertEquals(result, expected)

    def test_is_end_session(self):
        response = {
            'response': {
                'shouldEndSession': True
            }
        }

        # Check new session
        result = session_utils.is_end_session(response)
        self.assertEquals(result, True)

        response['response']['shouldEndSession'] = False
        result = session_utils.is_end_session(response)
        self.assertEquals(result, False)

    def test_get_intent_name(self):
        expected = 'intent_name'
        intent = {
            'name': expected
        }

        result = session_utils.get_intent_name(intent)
        self.assertEquals(result, expected)

    def test_get_number_value(self):
        expected = 123
        intent = {
            'slots': {
                'number': {
                    'value': expected
                }
            }
        }

        result = session_utils.get_number_value(intent)
        self.assertEquals(result, expected)
