import decimal
from math import pi

from great_circle_calculator.__error_checking import _check_point


def _degrees_to_radians(degrees):
    """ Converts the degrees into radians
    :param degrees: decimal degrees
    :return: radians
    """
    return decimal.Decimal(pi) * decimal.Decimal(degrees) / decimal.Decimal(180)


def _radians_to_degrees(radians):
    """ Converts the radians into degrees
    :param radians: decimal degrees
    :return: radians
    """
    return decimal.Decimal(180) * decimal.Decimal(radians) / decimal.Decimal(pi)


def _point_to_radians(point):
    point = _check_point(point)
    return (_degrees_to_radians(point[0]), _degrees_to_radians(point[1]))


def _point_to_degrees(point):
    return (_radians_to_degrees(point[0]), _radians_to_degrees(point[1]))