from unittest import TestCase
from mylawn.mylawn import water_guidance


class TestWater_guidance(TestCase):
    def test_water_guidance(self):
        assert water_guidance(100) == 1.5
        assert water_guidance(94) == 1.5
        assert water_guidance(89) == 1.25