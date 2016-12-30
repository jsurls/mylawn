from __future__ import absolute_import
import unittest

from mylawn.alexa_intents import on_stop, on_cancel, on_help


class AlexaIntentsTests(unittest.TestCase):
    def test_on_stop(self):
        result = on_stop(None, None)
        self.assertIsNotNone(result)

        should_end_session = result['response']['shouldEndSession']
        self.assertTrue(should_end_session)

    def test_on_cancel(self):
        result = on_cancel(None, None)
        self.assertIsNotNone(result)

        should_end_session = result['response']['shouldEndSession']
        self.assertTrue(should_end_session)

    def test_on_help(self):
        result = on_help(None, None)
        self.assertIsNotNone(result)

        should_end_session = result['response']['shouldEndSession']
        self.assertFalse(should_end_session)
