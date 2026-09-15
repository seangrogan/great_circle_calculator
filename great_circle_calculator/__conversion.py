from __future__ import annotations

from great_circle_calculator._constants import pi
from great_circle_calculator.__error_checking import Point, _error_check_point


def _degrees_to_radians(degrees: float) -> float:
    """Converts degrees into radians."""
    return pi * degrees / 180.0


def _radians_to_degrees(radians: float) -> float:
    """Converts radians into degrees."""
    return 180.0 * radians / pi


def _point_to_radians(point: Point) -> Point:
    point = _error_check_point(point)
    return _degrees_to_radians(point[0]), _degrees_to_radians(point[1])


def _point_to_degrees(point: Point) -> Point:
    return _radians_to_degrees(point[0]), _radians_to_degrees(point[1])
