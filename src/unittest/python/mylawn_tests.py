from __future__ import absolute_import
import unittest

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
