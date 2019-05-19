from __future__ import absolute_import

import unittest
import mock

import mylawn
from mylawn import water_guidance, mow_guidance


class MyLawnTests(unittest.TestCase):
    def test_water_guidance(self):
        self.assertEqual(water_guidance(100), 1.5)
        self.assertEqual(water_guidance(94), 1.5)
        self.assertEqual(water_guidance(89), 1.25)

    def test_mow_guidance(self):
        self.assertEqual(mow_guidance(100), "highest")
        self.assertEqual(mow_guidance(96), "highest")
        self.assertEqual(mow_guidance(95), "regular")
        self.assertEqual(mow_guidance(84), "regular")
        self.assertEqual(mow_guidance(83), "lowest")

    def test_mow_message(self):
        message = mylawn.mow_message(100)

        self.assertIsNotNone(message)
        self.assertTrue(message.startswith("You should mow at the"))

    def test_weather_message(self):
        message = mylawn.weather_message(100, 5)

        self.assertIsNotNone(message)
        self.assertTrue(message.startswith("The avg high was"))

    @mock.patch('mylawn.get_weather_data')
    def test_get_water_info(self, mock_get_weather_data):
        mock_get_weather_data.return_value = (100, 5)

        message = mylawn.get_water_info('station_id')

        self.assertIsNotNone(message)
        self.assertEquals(len(message), 3)
        self.assertTrue(message[0].startswith("The avg high was"))
