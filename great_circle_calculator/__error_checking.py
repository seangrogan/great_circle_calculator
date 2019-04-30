import warnings


def _check_points(*points):
    for point in points:
        yield _check_point(point)


def _check_point(point, *, correct_point=True):
    if len(point) != 2 and len(point) != 3:
        e_msg = f"Point should be length 2.  Point provided is of length {len(point)} and has the value of {point}"
        raise ValueError(e_msg)
    if len(point) == 3:
        w_msg = "Point should be length 2.  Point provided has a length of 3. " \
                "We will assume the third element is an elevation measurement and will be discarded"
        warnings.warn(w_msg)
    lon, lat, *_ = point
    if -90 <= lon <= 90 and -180 <= lat <= 180:  # The point is (probably!) reversed
        if correct_point:
            w_msg = "Point is probably reversed"
            warnings.warn(w_msg)
            return lat, lon
        else:
            e_msg = "Point's values do not make sense.  They are not on the Great Circle"
            raise ValueError(e_msg)
    return point


def _test_domain(x):
    if x > 1:
        return 1
    if x < -1:
        return -1
    return x
