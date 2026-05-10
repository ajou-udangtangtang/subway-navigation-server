import math


Point = tuple[float, float]


def angle_between(p_from: Point, p_to: Point) -> float:
    """Absolute bearing from p_from to p_to in [0, 360).

    Convention: north = 0°, east = 90°, south = 180°, west = 270°
    (clockwise positive). Matches the phone compass.

    math.atan2 returns angle measured CCW from +x (east), so we convert.
    """
    dx = p_to[0] - p_from[0]
    dy = p_to[1] - p_from[1]
    raw = math.degrees(math.atan2(dy, dx))
    bearing = (90.0 - raw) % 360.0
    return bearing
