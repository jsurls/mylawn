from mylawn.mylawn import water_guidance


def test_water_guidance():
    assert water_guidance(100) == 1.5
    assert water_guidance(94) == 1.5
    assert water_guidance(89) == 1.25