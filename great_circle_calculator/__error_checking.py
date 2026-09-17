from __future__ import annotations

import warnings


Point = tuple[float, float]


def _handle_point(obj):
    """
    Function used to process if a passed "point" is a shapely Point type/class

    The program ultimately will use native python types for returning
    """

    if hasattr(obj, "__geo_interface__"):
        geo = obj.__geo_interface__
        if geo["type"] != "Point":
            raise TypeError(f"Expected a Point, got {geo['type']}")
        x, y = geo["coordinates"][:2]
    elif isinstance(obj, (tuple, list)) and len(obj) >= 2:
        x, y = obj[0], obj[1]
    else:
        raise TypeError(f"Cannot interpret {type(obj)} as a point")
    return x, y

def _error_check_point(point: Point, correct_point: bool = False) -> Point:
    point = _handle_point(point)
    if len(point) != 2:
        raise TypeError(f"Point {point!s} is incorrect length!")
    lon, lat = float(point[0]), float(point[1])
    if -90 <= lat <= 90 and -180 <= lon <= 180:  # Point makes sense
        return lon, lat
    elif -90 <= lon <= 90 and -180 <= lat <= 180:  # The point is (probably!) reversed
        _msg = (
            f"Point {point!s} is probably reversed!\n\n"
            f"We believe that this is the case because "
            f"the provided longitude ({lon}) is in the range of [-90, 90] "
            f"and the provided latitude ({lat}) is in the range of [-180, 180].\n\n"
            f"The point must be provided as an iterable or tuple of length 2, where the "
            f"first element is the longitude in the range of [-180, 180], and "
            f"the second element is the latitude in the range of [-90, 90]."
        )
        if correct_point:
            warnings.warn(_msg)
            warnings.warn(
                "The parameter 'correct_point' has been set to True,\n"
                "Therefore we are reversing the point and continuing..."
            )
            return lat, lon
        raise ValueError(_msg)
    else:
        raise ValueError(
            f"\n"
            f"Point {point!s} cannot be appropriately interpreted in this program.\n\n"
            f"Be advised, the point must be provided as a tuple of length 2, where the "
            f"first element is the longitude in the range of [-180, 180], and "
            f"the second element is the latitude in the range of [-90, 90]).\n"
        )
