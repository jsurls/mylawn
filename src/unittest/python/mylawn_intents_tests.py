from __future__ import absolute_import

import mock
import unittest
import helper

from mylawn_intents import get_weather_data, set_station_from_zip


class MyLawnIntentsTest(unittest.TestCase):
    @mock.patch('mylawn_intents.get_water_info')
    @mock.patch('mylawn_intents.datastore')
    def test_get_weather_data(self, mock_datastore, mock_water_info):
        # set up the mock
        mock_datastore.get_user.return_value = {"userId": "123", "station_id": "12345"}
        mock_water_info.return_value = ["It's cold.", "Don't water.", "Don't mow."]

        session = helper.session("get_water_guide.json")

        result = get_weather_data(session)

        # we should have a result
        self.assertIsNotNone(result)

        # end the session
        should_end_session = result['response']['shouldEndSession']
        self.assertTrue(should_end_session)

    @mock.patch('mylawn_intents.datastore')
    def test_get_weather_data_with_user_without_station(self, mock_datastore):
        # set up the mock
        mock_datastore.get_user.return_value = {"userId": "123"}

        session = helper.session("get_water_guide.json")

        result = get_weather_data(session)

        # we should have a result
        self.assertIsNotNone(result)

        # don't end session
        should_end_session = result['response']['shouldEndSession']
        self.assertFalse(should_end_session)

    @mock.patch('mylawn_intents.datastore')
    def test_get_weather_data_with_no_user_data(self, mock_datastore):
        # set up the mock
        mock_datastore.get_user.return_value = None

        session = helper.session("get_water_guide.json")

        result = get_weather_data(session)

        # we should have a result
        self.assertIsNotNone(result)

        # don't end session
        should_end_session = result['response']['shouldEndSession']
        self.assertFalse(should_end_session)

    # ------- set station tests ----------

    @mock.patch('mylawn_intents.datastore')
    def test_set_station(self, mock_datastore):
        ask = helper.alexa_skills_request("set_station_from_zip.json")

        result = set_station_from_zip(ask['request']['intent'], ask['session'])

        # we should have a result
        self.assertIsNotNone(result)

        # end the session
        should_end_session = result['response']['shouldEndSession']
        self.assertTrue(should_end_session)

    @mock.patch('mylawn_intents.datastore')
    def test_set_station_bad_zip(self, mock_datastore):
        ask = helper.alexa_skills_request("set_station_from_zip_bad.json")

        result = set_station_from_zip(ask['request']['intent'], ask['session'])

        # we should have a result
        self.assertIsNotNone(result)

        # do not end the session
        should_end_session = result['response']['shouldEndSession']
        self.assertFalse(should_end_session)

