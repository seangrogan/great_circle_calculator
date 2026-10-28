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

def _format_output(point: Point, lat_lon: bool) -> Point:
    """Flip an internal (lon, lat) result back to (lat, lon) if the caller works that way."""
    return (point[1], point[0]) if lat_lon else point

def _error_check_point(point: Point, lat_lon: bool = False) -> Point:
    point = _handle_point(point)
    if lat_lon:
        point = point[1], point[0]   # caller gave (lat, lon); flip to internal (lon, lat)
    if len(point) != 2:
        raise TypeError(f"Point {point!s} is incorrect length!")
    lon, lat = float(point[0]), float(point[1])
    if -90 <= lat <= 90 and -180 <= lon <= 180:  # Point makes sense
        return lon, lat
    elif -90 <= lon <= 90 and -180 <= lat <= 180:  # The point is (probably!) reversed
        _msg = f"Point {point!s} is probably reversed!\n\n"
        _msg += f"We believe that this is the case because "\
            f"the provided longitude ({lon}) is in the range of [-90, 90] "\
            f"and the provided latitude ({lat}) is in the range of [-180, 180].\n\n"
        if lat_lon:
            _msg += f"the parameter {lat_lon=} was passed so we expect the point"\
                    f"{point!s} to be in the form (lat, lon).\n"\
                    f"Either leave the parameter lat_lon default or lat_lon=False to correct this error"
        else:
            _msg += f"By default, the program expects points to be in the form of (lon, lat).\n"\
                    "If you would like to not change the format the points are passed as, the parameter lat_lon=True can be passed"
        raise ValueError(_msg)
    else:
        raise ValueError(
            f"\n"
            f"Point {point!s} cannot be appropriately interpreted in this program.\n\n"
            f"Be advised, the point must be provided as a tuple of length 2, where the "
            f"first element is the longitude in the range of [-180, 180], and "
            f"the second element is the latitude in the range of [-90, 90]).\n"
        )
