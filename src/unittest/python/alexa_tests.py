from __future__ import absolute_import

import mock
import unittest
import helper

from alexa import lambda_handler


class AlexaTest(unittest.TestCase):
    @mock.patch('alexa.get_weather_data')
    def test_lambda_handler_intent_request(self, mock_get_weather_data):
        # set up the mock
        expected_response = {"response": {"shouldEndSession": True}};
        mock_get_weather_data.return_value = expected_response
        request = helper.alexa_skills_request("get_water_guide.json")

        result = lambda_handler(request, None)

        # we should have a result
        self.assertEqual(result, expected_response)

    def test_lambda_handler_stop_request(self):
        request = helper.alexa_skills_request("stop.json")
        expected = {'version': '1.0', 'response': {'shouldEndSession': True}, 'sessionAttributes': {}}

        result = lambda_handler(request, None)

        # we should have a result
        self.assertEqual(result, expected)

    def test_lambda_handler_cancel_request(self):
        request = helper.alexa_skills_request("cancel.json")
        expected = {'version': '1.0', 'response': {'shouldEndSession': True}, 'sessionAttributes': {}}

        result = lambda_handler(request, None)

        # we should have a result
        self.assertEqual(result, expected)

    def test_lambda_handler_help_request(self):
        request = helper.alexa_skills_request("get_help.json")

        result = lambda_handler(request, None)

        # we should have a result and end the session
        self.assertIsNotNone(result)
        self.assertFalse(result['response']['shouldEndSession'])

    @mock.patch('alexa.get_weather_data')
    def test_lambda_handler_catches_all_exceptions(self, mock_get_weather_data):
        # set up the mock
        mock_get_weather_data.return_value = Exception('mock exception raised')
        request = helper.alexa_skills_request("get_water_guide.json")

        result = lambda_handler(request, None)

        # we should have a result
        self.assertIsNotNone(result)

