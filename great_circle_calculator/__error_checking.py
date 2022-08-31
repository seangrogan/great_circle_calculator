import warnings


def _error_check_point(point, correct_point=False):
    if len(point) != 2:
        raise TypeError(f"Point {str(point)} is incorrect length!")
    lon, lat = float(point[0]), float(point[1])
    if -90 <= lat <= 90 and -180 <= lon <= 180:  # Point makes sense
        return (lon, lat)
    elif -90 <= lon <= 90 and -180 <= lat <= 180:  # The point is (probably!) reversed
        _msg = f"Point {str(point)} is probably reversed!\n\n" \
               f"We believe that this is the case because\n" \
               f"the provided longitude ({lon}) is in the range of [-90, 90]\n" \
               f"and the provided latitude ({lat}) is in the range of [-180, 180].\n\n" \
               f"The pont must be provided as a tuple of length 2, where the\n" \
               f"first element is the longitude in the range of [-180, 180], and\n" \
               f"the second element is the latitude in the range of [-90, 90].\n"

        if correct_point:
            warnings.warn(_msg)
            warnings.warn(f"The parameter 'correct_point' has been set to True,\n"
                          f"Therefore we are reversing the point and continuing...")
            point_corrected = (lat, lon)
            return point_corrected
        else:
            raise ValueError(_msg)
    else:
        raise ValueError(f"\n"
                         f"Point {str(point)} cannot be appropriately interpreted in this program.\n"
                         f"Be advised, the pont must be provided as a tuple of length 2, where the\n"
                         f"first element is the longitude in the range of [-180, 180], and\n"
                         f"the second element is the latitude in the range of [-90, 90]).\n")
