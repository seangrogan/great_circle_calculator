def _error_check_point(point, correct_point=True):
    if len(point) != 2:
        print("Point", str(point), "is incorrect length!")
        return False
    lon, lat = point[0], point[1]
    if -90 <= lat <= 90 and -180 <= lon <= 180:  # Point makes sense
        return point
    elif -90 <= lon <= 90 and -180 <= lat <= 180:  # The point is (probably!) reversed
        print("Point", str(point), "is probably reversed!")
        if correct_point:
            point_corrected = (lat, lon)
            return point_corrected
        return False
    else:
        print("Point", str(point), "Cannot be interpreted!")
        return False
