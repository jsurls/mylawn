from mylawn.mylawn import mow_guidance


def test_mow_guidance():
    assert mow_guidance(100) == "highest"
    assert mow_guidance(96) == "highest"
    assert mow_guidance(95) == "regular"
    assert mow_guidance(84) == "regular"
    assert mow_guidance(83) == "lowest"
