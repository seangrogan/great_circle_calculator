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

#### Function `distance_between_points()`

Function `distance_between_points(p1, p2, unit='meters', haversine=True)` computes the distance between two points in the unit given in the unit parameter.  It will calculate the distance using the law of cosines unless the user specifies `haversine` to be `true`.  `p1` and `p2` are points (i.e. tuples, lists of length 2) in the form of (lon, lat) in decimal degrees (That is, a tuple of float values, the library cannot handle DMS data).  `unit` is a unit of measurement that can be accessed by [`great_circle_calculator.constants.eligible_units`](#eligible_units), default is `'meters'`.  `haversine=True` uses the [haversine](https://en.wikipedia.org/wiki/Haversine_formula) formula, which is consideered superior for short distances (which is my often use case).  Changing it to `haversine=False` yeilds the [law of cosines](https://en.wikipedia.org/wiki/Spherical_law_of_cosines) which, typically, will have a quicker computational time.  

#### Function `bearing_at_p1()`

Function  `bearing_at_p1(p1, p2)` computes the bearing (i.e. course) at p1 given a destination of p2.  Use in conjunction with [`midpoint()`](#midpoint) and [`intermediate_point()`](#intermediate_point) to find the course along the route.  Use [`bearing_at_p2()`](#bearing_at_p2) to find the bearing at the endpoint, `p2`.  `p1` and `p2` are points (i.e. tuples, lists of length 2) in the form of (lon, lat) in decimal degrees.  

Example to find a course enroute:

```python
import great_circle_calculator.great_circle_calculator as gcc
""" This code snippit will find the the course at a point p3 which is 20% the way between points p1 and p2
"""
p1, p2 = (lon1, lat1), (lon2, lat2)
frac_along_route = 0.2
course_enroute = gcc.bearing_at_p1(gcc.intermediate_point(p1, p2, frac_along_route), p2)
```
#### Function `bearing_at_p2`

Function  `bearing_at_p2(p1, p2)` computes the bearing (i.e. course) at p2 given a start of p1.  Use in conjunction with [`midpoint()`](#midpoint) and [`intermediate_point()`](#intermediate_point) to find the course along the route.  Use [`bearing_at_p1()`](#bearing_at_p1) to find the bearing at the starting point, `p1`.  `p1` and `p2` are points (i.e. tuples, lists of length 2) in the form of (lon, lat) in decimal degrees.  
        
#### Function `midpoint()`

Function `midpoint(p1, p2)` is the half-way point along a great circle path between the two points.  `p1` and `p2` are points (i.e. tuples, lists of length 2) in the form of (lon, lat) in decimal degrees.  For example, say `p3 = midpoint(p1, p2)`, `distance_between_points(p1, p3) == distance_between_points(p2, p3)` 

#### Function `intermediate_point()`

Function intermediate_point(p1, p2, fraction=0.5) an intermediate point along the course laid out by `p1` to `p2` given the fractional distance.  `fraction` is the fraction of the distance between `p1` and `p2`, where 0 is `p1`, 0.5 is equivalent to [`midpoint()`](#midpoint), and 1 is `p2`.  

#### Function `point_given_start_and_bearing()`
        
Function point_given_start_and_bearing(p1, course, distance, unit='meters') is given a start point `p1`, initial bearing `course`, and distance `distance`, this will calculate the destination point bearing travelling along a (shortest distance) great circle arc.  `unit` is a unit of measurement that can be accessed by [`great_circle_calculator.constants.eligible_units`](#eligible_units), default is `'meters'`.
    
 ### Library `compass`
 
 This libaray was created to let me call, say `Compass.east` so I can get 90deg.  I thought it helped with code readability 
 at first, kept it because it might be useful...   
 
 It has two classes called `CompassSimple` and `CompassComplex`.  `CompassComplex` is still in the todo list but it contains more information about each compass point.  
 
 To see the eligble points, see [here](https://en.wikipedia.org/wiki/Points_of_the_compass#32_compass_points).  Simply use the terms in "Compass point", use lower case and underscores where there are spaces or dashes.  Alternatively you may use the "Abbreviation" with the appropriate case to call the same value.  
 
 To use `CompassSimple`:
 
 ```python
import great_circle_calculator.CompassSimple as compass

print(compass.east)  # prints 90
print(compass.north)  # prints 0
print(compass.northwest_by_north)  # prints 326.250
print(compass.SEbE)  # Southeast by east, prints 123.750
print(compass.SWbS == compass.southwest_by_south)  # prints True
```

  
 ### Library `_constants`
 
 This was created for two purposes:
 
 1) To easily store the radius of the earth in various units
 
 2) To simplify the code in the program so I don't have to call `math.*` each time I want sin, cos, etc.
 
 To see the available units, call `_constants.eligible_units` and a list of the units that are available will be given. 
 
 ###### `eligible_units`
 
 To see the available units, call `_constants.eligible_units` and a list of the units that are available will be given. 
 
 ### Libraries  `__conversion` and `__error_checking`
 
 Private libraries that convert (`__conversion.py`) values between radians and degrees as the default option 
 for python's math package is radians.  
 
 The error checking library (`__error_checking.py`) is something I want to work on.  I use regular cartesian convention 
 when passing points, i.e. (lon, lat) or (x, y).  So if you try to pass a point which is in (lat, lon) and it doesn't 
 pass the sanity check, such as lat > 90 and lon <= 90, it will, right now, swap the coordinates.  Not sure if that's 
 the best for everyone, but I am mostly working on projects where the lon is (approximately) > 90 
 
 ## And finally...
 
 Package last updated Mar 4, 2021.  Readme last updated Mar 4, 2021.  
 
 ## Change Log
 
 * 1.2.0 - If the user sends a point that is `decimal` data type, it will convert to a tuple of `float` types.  Updated the readme for clarity  
 * 1.1.0 - Changed `haversine=True` as the default for [`distance_between_points`](#distance_between_points) as it more accurately reflects the small distance calculation I am using in my projects.
 * 1.0.2 - squished an error in the intermediate function. The number of errors has been embarrassing. I hope you won't judge me too harshly.  
 * 1.0.1.post1 - includes a domain checker for `asin()` and `acos()` because rounding errors can cause the function to be out of range.
 * 1.0.post1 - I screwed up the numbering order, still new at this... please ignore.
 * 1.0.1 - Fixed an error in the (`point_given_start_and_bearing`)[#point_given_start_and_bearing]
 * 1.0.0 - First Edition, inital commit, etc.
 
 
   
 
    
