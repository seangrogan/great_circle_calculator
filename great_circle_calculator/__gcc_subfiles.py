from math import sin, cos, atan2, sqrt, acos, asin as _asin, atan as _atan

from great_circle_calculator.__deg_rad_converter import _radians_to_degrees
from great_circle_calculator.__error_checking import _test_domain


def __haversine(lon1, lat1, lon2, lat2, r_earth):
    d_lat, d_lon = lat2 - lat1, lon2 - lon1
    a = sin(d_lat / 2) * sin(d_lat / 2) + cos(lat1) * cos(lat2) * sin(d_lon / 2) * sin(d_lon / 2)
    c = 2 * atan2(sqrt(a), sqrt((1 - a)))
    dist = r_earth * c
    return dist


def __spherical_law_of_cosines(lon1, lat1, lon2, lat2, r_earth):
    dist = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)) * r_earth
    return dist


def asin(x):
    _asin(_test_domain(x))


def atan(x):
    _atan(_test_domain(x))


def _midpoint_lat(lat1, lat2, b_x, b_y):
    lat = atan2(sin(lat1) + sin(lat2), sqrt((cos(lat1) + b_x) * (cos(lat1) + b_x) + b_y * b_y))
    lat = _radians_to_degrees(lat)
    return lat


def _midpoint_lon(lon1, b_y, lat1, b_x):
    lon = lon1 + atan2(b_y, cos(lat1) + b_x)
    lon = (_radians_to_degrees(lon) + 540) % 360 - 180
    return lon