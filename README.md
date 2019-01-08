# Great Circle Calculator

 This is a collection of equations and formulas that I've been using across many projects to compute various 
 distances using great circle calculations. The formulas here were adapted into python for my use from 
 [here](https://www.movable-type.co.uk/scripts/latlong.html) and [here](http://www.edwilliams.org/avform.htm).   
 Because I've been using these equations across several projects, I decided to upload this to PyPI for ease of 
 keeping updated and distribution. Feel free to clone, fork, or modify the code as needed.  I believe there are 
 more robust packages out there.  One example is [geodesy](https://github.com/chrisveness/geodesy).  
 But I figured I could use the python practice.   
 
 Any questions, feel free to get in touch.
 
 ## How to install
 
 I still haven't uploaded it to the PyPI as of this writing.  But you can either download/clone the package to 
 your computer or download it via pip install (someday).
 
 ## How to use
 
 Right now, there aren't that many functions to go over, but I'll outline them here.  
 
 ### Library `great_circle_calculator`
 
    distance_between_points(p1, p2, unit='meters', haversine=False):
        This function computes the distance between two points in the unit given in the unit parameter.  It will calculate the distance using the law of cosines unless the user specifies haversine to be true.
            :param p1: tuple point of (lon, lat)
            :param p2: tuple point of (lon, lat)
            :param unit: unit of measurement. List can be found in constants.eligible_units
            :param haversine: False (default) uses law of cosines, True uses haversine
            :return: Distance between p1 and p2 in the units specified.
    
    bearing_at_p1(p1, p2):
        This function computes the bearing (i.e. course) at p1 given a destination of p2.  Use in conjunction with
        midpoint(*) and intermediate_point(*) to find the course along the route.  Use bearing_at_p2(*) to find the bearing
        at the endpoint
            :param p1: tuple point of (lon, lat)
            :param p2: tuple point of (lon, lat)
            :return: Course, in degrees
            
    bearing_at_p2(p1, p2):
        This function computes the bearing (i.e. course) at p2 given a starting point of p1.  Use in conjunction with
        midpoint(*) and intermediate_point(*) to find the course along the route.  Use bearing_at_p1(*) to find the bearing
        at the endpoint
            :param p1: tuple point of (lon, lat)
            :param p2: tuple point of (lon, lat)
            :return: Course, in degrees
        
    
    midpoint(p1, p2):
        This is the half-way point along a great circle path between the two points.
            :param p1: tuple point of (lon, lat)
            :param p2: tuple point of (lon, lat)
            :return: point (lon, lat)
            
    intermediate_point(p1, p2, fraction=0.5):
        This function calculates the intermediate point along the course laid out by p1 to p2.  fraction is the fraction
        of the distance between p1 and p2, where 0 is p1, 0.5 is equivalent to midpoint(*), and 1 is p2.
            :param p1: tuple point of (lon, lat)
            :param p2: tuple point of (lon, lat)
            :param fraction: the fraction of the distance along the path.
            :return: point (lon, lat)
        
    point_given_start_and_bearing(p1, course, distance, unit='meters'):
        Given a start point, initial bearing, and distance, this will calculate the destina­tion point and final
        bearing travelling along a (shortest distance) great circle arc.
            :param p1: tuple point of (lon, lat)
            :param course: Course, in degrees
            :param distance: a length in unit
            :param unit: unit of measurement. List can be found in constants.eligible_units
            :return: point (lon, lat)
    
 ### Library `compass`
 
 This lets me call something like `Compass.east` so I can get 90deg.  I thought it helped with code readability 
 at first, kept it because it might be useful...   
  
 ### Library `_constants`
 
 This was created for two purposes:
 
 1) To easily store the radius of the earth in various units
 
 2) To simplify the code in the program so I don't have to call `math.*` each time I want sin, cos, etc.
 
 To see the available units, call `_constants.eligible_units` and a list of the units that are available will be given. 
 
 ### Libraries  `__conversion` and `__error_checking`
 
 Private libraries that convert (`__conversion.py`) values between radians and degrees as the default option 
 for python's math package is radians.  
 
 The error checking library (`__error_checking.py`) is something I want to work on.  I use regular cartesian convention 
 when passing points, i.e. (lon, lat) or (x, y).  So if you try to pass a point which is in (lat, lon) and it doesn't 
 pass the sanity check, such as lat > 90 and lon <= 90, it will, right now, swap the coordinates.  Not sure if that's 
 the best for everyone, but I am mostly working on projects where the lon is (approximately) > 90 
 
 ## And finally:
 
 Last updated Jan 8, 2018.  Hit me up here for questions and critiques.  
 
   
 
    