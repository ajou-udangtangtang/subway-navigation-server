"""Pin the coordinate convention: north=0°, east=90°, south=180°, west=270°.

This test file is a contract — changing the convention requires team agreement
(see docs/09-위험요소및결정항목.md D-01).
"""

import pytest

from subway_server.core.direction import angle_between


def test_north_is_0():
    assert angle_between((0, 0), (0, 1)) == pytest.approx(0.0)


def test_east_is_90():
    assert angle_between((0, 0), (1, 0)) == pytest.approx(90.0)


def test_south_is_180():
    assert angle_between((0, 0), (0, -1)) == pytest.approx(180.0)


def test_west_is_270():
    assert angle_between((0, 0), (-1, 0)) == pytest.approx(270.0)


def test_northeast_is_45():
    assert angle_between((0, 0), (1, 1)) == pytest.approx(45.0)


def test_northwest_is_315():
    assert angle_between((0, 0), (-1, 1)) == pytest.approx(315.0)


def test_southeast_is_135():
    assert angle_between((0, 0), (1, -1)) == pytest.approx(135.0)


def test_southwest_is_225():
    assert angle_between((0, 0), (-1, -1)) == pytest.approx(225.0)


def test_returns_in_zero_360_range():
    # Sweep many directions; output must always be in [0, 360).
    import math
    for deg in range(0, 360, 7):
        rad = math.radians(deg)
        # Build a target on unit circle around origin in standard math frame.
        x = math.cos(rad)
        y = math.sin(rad)
        result = angle_between((0, 0), (x, y))
        assert 0.0 <= result < 360.0


def test_translation_invariance():
    # Same direction from different origins.
    a = angle_between((0, 0), (1, 0))
    b = angle_between((100, 100), (101, 100))
    assert a == pytest.approx(b)
