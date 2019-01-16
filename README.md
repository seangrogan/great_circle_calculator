# Great Circle Calculator


 This is a collection of equations and formulas that I've been using across my many projects to compute various 
 distances using great circle calculations. The formulas here were adapted into python from 
 [here](https://www.movable-type.co.uk/scripts/latlong.html) and [here](http://www.edwilliams.org/avform.htm).   
 
 Because I've been using these equations across several projects, I decided to upload this to PyPI for ease of 
 keeping updated and distribution. Feel free to clone, fork, or modify the code as needed.  I believe there are 
 more robust packages out there.  One example is [geodesy](https://github.com/chrisveness/geodesy).  
 But I figured I could use the python practice.   
 
 Any questions, feel free to get in touch.
 
 ## How to install
 
Clone/download the package to your project or use `pip install great-circle-calculator` ([PyPI](https://pypi.org/project/great-circle-calculator/))
 
 ## How to use
 
 Here is an outline of the functions available to you. 
 
 ### Library `great_circle_calculator`
 
 Depending on my needs, I will either import this library as 
 
```python
import great_circle_calculator.great_circle_calculator as gcc
```

or 

```python
from great_circle_calculator.great_circle_calculator import *
```

where * can be a specific function (or left as * for all the functions)

The functions are [distance_between_points](#distance_between_points), [bearing_at_p1](#bearing_at_p1), [bearing_at_p2](#bearing_at_p2), [midpoint](#midpoint),[ intermediate_point](#intermediate_point), [point_given_start_and_bearing](#point_given_start_and_bearing)

#### `distance_between_points()`

Function `distance_between_points(p1, p2, unit='meters', haversine=True)` computes the distance between two points in the unit given in the unit parameter.  It will calculate the distance using the law of cosines unless the user specifies `haversine` to be `true`.  `p1` and `p2` are points (i.e. tuples, lists of length 2) in the form of (lon, lat) in decimal degrees.  `unit` is a unit of measurement that can be accessed by [`great_circle_calculator.constants.eligible_units`](#eligible_units), default is `'meters'`.  `haversine=True` uses the [haversine](https://en.wikipedia.org/wiki/Haversine_formula) formula, which is consideered superior for short distances (which is my often use case).  Changing it to `haversine=False` yeilds the [law of cosines](https://en.wikipedia.org/wiki/Spherical_law_of_cosines) which typically, will have a quicker computational time.  


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
 
 ###### eligible_units
 
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
 
   
 
    
