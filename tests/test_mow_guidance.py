from unittest import TestCase
from mylawn.mylawn import mow_guidance


class TestMow_guidance(TestCase):
    def test_mow_guidance(self):
        assert mow_guidance(100) == "highest"
        assert mow_guidance(96) == "highest"
        assert mow_guidance(95) == "regular"
        assert mow_guidance(84) == "regular"
        assert mow_guidance(83) == "lowest"
