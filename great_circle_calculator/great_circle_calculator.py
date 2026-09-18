"""Great-circle math: distance, bearing, midpoint, and interpolation between (lon, lat) points.

New for Version 2 : By default all distance-based functions use Earth as the reference sphere,
but there have been two ways added to change the reference sphere!

There is a new parameter 'planet_radius' that takes a positive, non-zero float or integer value.

The second is passing a 'body' parameter which takes a built-in class:
'great_circle_calculator.celestial_body.CelestialBody' class.

You can also use non-meter units in the calculations.
See great_circle_calculator._constants.eligible_units() for eligible units and
great_circle_calculator._constants.register_unit to add your own.
"""
from __future__ import annotations

from great_circle_calculator.__conversion import _point_to_radians
from great_circle_calculator.__conversion import _point_to_degrees
from great_circle_calculator.__conversion import _radians_to_degrees
from great_circle_calculator.__conversion import _degrees_to_radians


from great_circle_calculator.__error_checking import Point, _error_check_point
from great_circle_calculator.celestial_body import CelestialBody, EARTH

from great_circle_calculator._constants import sin, asin, cos, acos, atan2, sqrt

def _resolve_radius(unit: str, planet_radius: float | None, body: CelestialBody) -> float:
    """Resolves the sphere radius to use, expressed in 'unit'.

    If 'planet_radius' is given, it's taken to already be expressed in 'unit' and used as-is
    (this is how you plug in a one-off custom sphere without building a CelestialBody).
    Otherwise, 'body's' radius is converted into 'unit' and used.
    """
    if planet_radius is not None:
        if planet_radius <= 0:
            raise ValueError("radius must be a positive number")
        return planet_radius
    return body.radius(unit)


def _central_angle(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """The angular separation (in radians) between two points, given as radians.
    This is independent of any particular sphere's radius, which is why
    functions like intermediate_point() don't need a unit/body/radius argument.
    """
    d_lat, d_lon = lat2 - lat1, lon2 - lon1
    a = sin(d_lat / 2) * sin(d_lat / 2) + cos(lat1) * cos(lat2) * sin(d_lon / 2) * sin(d_lon / 2)
    a = min(1.0, a)
    return 2 * atan2(sqrt(a), sqrt(1 - a))


def distance_between_points(
    p1: Point | tuple,
    p2: Point | tuple,
    unit: str = "meters",
    haversine: bool = True,
    planet_radius: float | None = None,
    body: CelestialBody = EARTH
) -> float:
    """Computes the distance between two points, in the unit given by the 'unit' parameter.
    Uses the haversine formula unless 'haversine' is set to False, in which case the
    (typically faster, less precise for short distances) law of cosines is used.

    :param p1: tuple point of (lon, lat)
    :param p2: tuple point of (lon, lat)
    :param unit: unit of measurement. See great_circle_calculator._constants.eligible_units()
    :param haversine: True (default) uses haversine distance, False uses law of cosines
    :param planet_radius: optional custom sphere radius, expressed in 'unit'. Overrides 'body'
        use this for a quick one-off body without constructing a CelestialBody.
    :param body: which CelestialBody's radius to use if 'planet_radius' isn't given. Defaults to
        Earth; pass e.g. 'great_circle_calculator.celestial_body.MARS' to compute distances on Mars.
    :return: Distance between p1 and p2, in 'unit'.

    New for version 2: can pass a Shapely Point class if that's how your data is stored.  You can also
    pass different radius or celestial body
    """
    lon1, lat1 = _point_to_radians(_error_check_point(p1))
    lon2, lat2 = _point_to_radians(_error_check_point(p2))
    r = _resolve_radius(unit, planet_radius, body)
    if haversine:
        c = _central_angle(lat1, lon1, lat2, lon2)
        return r * c
    # Spherical law of cosines
    return acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)) * r


def bearing_at_p1(p1: Point, p2: Point) -> float:
    """Computes the bearing (i.e. course) at p1 given a destination of p2. Use in conjunction
    with midpoint() and intermediate_point() to find the course along the route. Use
    bearing_at_p2() to find the bearing at the endpoint.

    :param p1: tuple point of (lon, lat)
    :param p2: tuple point of (lon, lat)
    :return: Course, in degrees
    """
    lon1, lat1 = _point_to_radians(_error_check_point(p1))
    lon2, lat2 = _point_to_radians(_error_check_point(p2))
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2 - lon1)
    y = sin(lon2 - lon1) * cos(lat2)
    course = atan2(y, x)
    return _radians_to_degrees(course)


def bearing_at_p2(p1: Point, p2: Point) -> float:
    """Computes the bearing (i.e. course) at p2 given a starting point of p1. Use in
    conjunction with midpoint() and intermediate_point() to find the course along the route.
    Use bearing_at_p1() to find the bearing at the starting point.

    Keep in mind! This is the direction you're facing when you walk the path between p1 and p2 and are
    standing at p2 (i.e. your back is toward p1)

    :param p1: tuple point of (lon, lat)
    :param p2: tuple point of (lon, lat)
    :return: Course, in degrees
    """
    return (bearing_at_p1(p2, p1) + 180) % 360


def midpoint(p1: Point, p2: Point) -> Point:
    """The half-way point along a great circle path between the two points.

    :param p1: tuple point of (lon, lat)
    :param p2: tuple point of (lon, lat)
    :return: point (lon, lat)
    """
    lon1, lat1 = _point_to_radians(_error_check_point(p1))
    lon2, lat2 = _point_to_radians(_error_check_point(p2))
    b_x = cos(lat2) * cos(lon2 - lon1)
    b_y = cos(lat2) * sin(lon2 - lon1)
    lat3 = atan2(sin(lat1) + sin(lat2), sqrt((cos(lat1) + b_x) * (cos(lat1) + b_x) + b_y * b_y))
    lon3 = lon1 + atan2(b_y, cos(lat1) + b_x)
    lat3 = _radians_to_degrees(lat3)
    lon3 = (_radians_to_degrees(lon3) + 540) % 360 - 180
    return lon3, lat3


def intermediate_point(p1: Point, p2: Point, fraction: float = 0.5) -> Point:
    """Calculates the intermediate point along the course laid out by p1 to p2. 'fraction'
    is the fraction of the distance between p1 and p2, where 0 is p1, 0.5 is equivalent to
    midpoint(), and 1 is p2. This is independent of any sphere's radius, so it works the same
    regardless of which planetary body the points are on.

    :param p1: tuple point of (lon, lat)
    :param p2: tuple point of (lon, lat)
    :param fraction: the fraction of the distance along the path. Must be between 0 and 1.
    :return: point (lon, lat)
    """
    if not 0 <= fraction <= 1:
        raise ValueError(f"fraction must be between 0 and 1 (inclusive); got {fraction}")
    lon1, lat1 = _point_to_radians(_error_check_point(p1))
    lon2, lat2 = _point_to_radians(_error_check_point(p2))
    delta = _central_angle(lat1, lon1, lat2, lon2)
    if delta == 0:
        # p1 and p2 are the same point; any fraction returns that point.
        return _point_to_degrees((lon1, lat1))
    a = sin((1 - fraction) * delta) / sin(delta)
    b = sin(fraction * delta) / sin(delta)
    x = a * cos(lat1) * cos(lon1) + b * cos(lat2) * cos(lon2)
    y = a * cos(lat1) * sin(lon1) + b * cos(lat2) * sin(lon2)
    z = a * sin(lat1) + b * sin(lat2)
    lat3 = atan2(z, sqrt(x * x + y * y))
    lon3 = atan2(y, x)
    return _point_to_degrees((lon3, lat3))


def point_given_start_and_bearing(
    p1: Point,
    course: float,
    distance: float,
    unit: str = "meters",
    planet_radius: float | None = None,
    body: CelestialBody = EARTH,
) -> Point:
    """Given a start point, initial bearing, and distance, calculates the destination point
    reached by traveling along a (shortest-distance) great circle arc.

    :param p1: tuple point of (lon, lat)
    :param course: Course, in degrees
    :param distance: distance to travel, in 'unit'
    :param unit: unit of measurement for 'distance'. See _constants.eligible_units()
    :param planet_radius: optional custom sphere radius, expressed in 'unit'. Overrides 'body'.
    :param body: which CelestialBody's radius to use if 'radius' isn't given. Defaults to Earth.
    :return: point (lon, lat)
    """
    lon1, lat1 = _point_to_radians(_error_check_point(p1))
    bearing = _degrees_to_radians(course)
    r = _resolve_radius(unit, planet_radius, body)
    delta = distance / r
    lat2 = asin(sin(lat1) * cos(delta) + cos(lat1) * sin(delta) * cos(bearing))
    lon2 = lon1 + atan2(sin(bearing) * sin(delta) * cos(lat1), cos(delta) - sin(lat1) * sin(lat2))
    lon2 = (_radians_to_degrees(lon2) + 540) % 360 - 180
    return lon2, _radians_to_degrees(lat2)

