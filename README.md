# Great Circle Calculator

 This is a collection of equations and formulas that I've been using across my many projects to compute various distances using great circle calculations. The formulas here were adapted into python from [here](https://www.movable-type.co.uk/scripts/latlong.html) and [here](http://www.edwilliams.org/avform.htm).   
 
 Because I've been using these equations across several projects, I decided to upload this to PyPI for ease of keeping updated and distribution. Feel free to clone, fork, or modify the code as needed.  I believe there are more complete packages out there.  One example is [geodesy](https://github.com/chrisveness/geodesy).  

 Part of the goal of this package was to be readily inspectable and self contained. There are no other dependencies required for this package to run.  
 
 Any questions, feel free to get in touch. Email and/or submit a bug report if you see any bugs.  
 
 ## How to install
 
Clone/download the package to your project or use `pip install great-circle-calculator` 

 * [PyPI](https://pypi.org/project/great-circle-calculator/)
 * [GitHub](https://github.com/seangrogan/great_circle_calculator)
 
 ## How to use
 
The convention of this package is for the spatial points to be represented as a tuple of length 2 with longitude being the first element and latitude being the second element, i.e. `(lon, lat)`. One should be able to pass a [Shapely](https://pypi.org/project/shapely/) [Point](https://shapely.readthedocs.io/en/stable/reference/shapely.Point.html) object if the point is in the form of `(lon, lat)` as well.

**NEW FOR 2.1** : functions that take a point or return a point now have the parameter `lat_lon`.  Set `lat_lon=True` to pass points in the form `(lat, lon)`.
 
 Here is an outline of the functions available to you. 
 
 ### Library `great_circle_calculator`
 
 Depending on my needs, I typically import this library as

```python
import great_circle_calculator as gcc
```

Although this convention does not need to be followed.  I will be using this convention in the samples below.  

The functions are 

 * [distance_between_points](#function-distance_between_points)
 * [bearing_at_p1](#function-bearing_at_p1)
 * [bearing_at_p2](#function-bearing_at_p2)
 * [midpoint](#function-midpoint)
 * [intermediate_point](#function-intermediate_point)
 * [point_given_start_and_bearing](#function-point_given_start_and_bearing)

#### Function `distance_between_points()`

Function 
```python
distance_between_points(
    p1: tuple | Point,
    p2: tuple | Point,
    unit: str = "meters",
    haversine: bool = True,  # False for law of cosines
    planet_radius: float | None = None,
    body: CelestialBody = EARTH,
    lat_lon: bool = False
)
```

Computes the distance between two points, in the unit given by the 'unit' parameter. 

Uses the **haversine** formula unless `haversine=False`, in which case the (typically faster, less precise for short distances) law of cosines is used. 

`p1`: tuple point of `(lon, lat)`. `p2`: tuple point of `(lon, lat)`.  **New for 2.1** Pass `lat_lon = True` to submit points as `(lat, lon)`. You can also pass a Shapely `Point` instead of a `tuple`.  

`unit`: unit of measurement. See `great_circle_calculator._constants.eligible_units()`.  You can also submit your own units. Typically full spellings are acceptable (`'kilometers'` or `'miles'`), American or British spellings are tolerated (`'meters'` or `'metres'`). Abbrivations can be passed.  I made the executive decision that `'nm'` is nautical miles rather than nanometers. Also Also keep in mind that a nautical mile here is defined as the international nautical mile. 

`planet_radius`: optional custom sphere radius, expressed in `unit` (Although `unit` has no effect if `planet_radius` is given, as the output will be in the units of the input unit). Parameter `planet_radius` Overrides `body`.  Use this when you don't want to construct a `CelestialBody`. 

`body`: which CelestialBody's radius to use if 'planet_radius' isn't given. Defaults to `EARTH`; pass e.g. `elestial_body.MARS` to compute distances on Mars. This returns a float which is the distance between `p1` and `p2`, in 'unit'.

Example: 

```python
import great_circle_calculator as gcc

p1 = (-73.569494, 45.496181)
p2 = (-73.993531, 40.750655)

# Standard Calculation
d1 = gcc.distance_between_points(p1, p2)
print(d1) # 528797.1333940749

# Using Law of Cosines, small difference at this distance at far too many significant figures to matter
d2 = gcc.distance_between_points(p1, p2, haversine=False)
print(d2) # 528797.1333940765

# Using the nautical mile
d3 = gcc.distance_between_points(p1, p2, unit='nautical_miles')
print(d3) # 285.5276098240145

# What if the same points were on Ganymede?
d4 = gcc.distance_between_points(p1, p2, body=gcc.celestial_body.GANYMEDE)
print(d4) # 218632.0089583005
```

#### Function `bearing_at_p1()`

```python
bearing_at_p1(
        p1: tuple | Point,
        p2: tuple | Point,
        lat_lon: bool = False
) -> float:
```

Function  `bearing_at_p1(p1, p2)` computes the bearing (course, compass direction) at p1 given a destination of p2.  Use in conjunction with [`midpoint()`](#function-midpoint) and/or[`intermediate_point()`](#function-intermediate_point) to find the course along the route.  Use [`bearing_at_p2()`](#function-bearing_at_p2) to find the bearing at the endpoint, `p2`.  `p1` and `p2` are points (i.e. tuples, lists of length 2) in the form of (lon, lat). **New for 2.1** Pass `lat_lon = True` to submit points as `(lat, lon)`. You can also pass a Shapely `Point` instead of a `tuple`.

```python
import great_circle_calculator as gcc

p1 = (-73.596622, 45.503519)
p2 = (  2.294895, 48.858060)

b1 = gcc.bearing_at_p1(p1, p2)
print(b1) # 57.06... about East North East
``` 

#### Function `bearing_at_p2`

```python
bearing_at_p1(
        p1: tuple | Point,
        p2: tuple | Point,
        lat_lon: bool = False
) -> float:
```

Function  `bearing_at_p2(p1, p2)` computes the bearing (i.e. course) at p2 given a start of p1.

Keep in mind that `bearing_at_p2(p1, p2)` _does not_ show the direction of you standing at `p2` and facing `p1`, but rather as if you're traveling _from_ `p1` to `p2`, what direction would you be facing at `p2` **New for 2.1** Pass `lat_lon = True` to submit points as `(lat, lon)`. You can also pass a Shapely `Point` instead of a `tuple`.

```python
import great_circle_calculator as gcc

p1 = (-73.596622, 45.503519)
p2 = (  2.294895, 48.858060)

b2 = gcc.bearing_at_p1(p1, p2)
print(b2) # 116.61... about East South East
``` 


#### Function `midpoint()`

Function `midpoint(p1, p2)` is the half-way point along a great circle path between the two points.  `p1` and `p2` are points (i.e. tuples, lists of length 2) in the form of (lon, lat) in decimal degrees.  For example, say `p3 = midpoint(p1, p2)`, `distance_between_points(p1, p3) == distance_between_points(p2, p3)` (although considering floating point maths, these will be close if not equal)

#### Function `intermediate_point()`

Function intermediate_point(p1, p2, fraction=0.5) an intermediate point along the course laid out by `p1` to `p2` given the fractional distance.  `fraction` is the fraction of the distance between `p1` and `p2`, where 0 is `p1`, 0.5 is equivalent to [`midpoint()`](#midpoint), and 1 is `p2`.  

#### Function `point_given_start_and_bearing()`
        
Function point_given_start_and_bearing(p1, course, distance, unit='meters') is given a start point `p1`, initial bearing `course`, and distance `distance`, this will calculate the destination point bearing travelling along a (shortest distance) great circle arc.  `unit` is a unit of measurement that can be accessed by [`great_circle_calculator.constants.eligible_units`](#eligible_units), default is `'meters'`.

#### Custom units

As of 2.0.0, `unit` is no longer limited to a fixed list. `great_circle_calculator.eligible_units()` returns the currently-registered unit names (a decent default set is built in: meters, kilometers, centimeters, millimeters, miles, feet, inches, yards, nautical_miles, fathoms, furlongs). Add your own with `register_unit`:

```python
import great_circle_calculator as gcc

gcc.register_unit('shufflin_step', 12)
p1 = (45.496547, -73.569841)
p2 = (40.750455, -73.993824)
gcc.distance_between_points(p1, p2) # 154703.2456...
gcc.distance_between_points(p1, p2, unit='shufflin_step') # 1856438.9473...
```

#### Other planetary bodies

`distance_between_points` and `point_given_start_and_bearing` accept a `body` parameter (default `EARTH`) so you can run the same great-circle math on other spheres. `MOON`, `MARS`, `VENUS`, and `MERCURY` are predefined, or build your own `CelestialBody`:

```python
import great_circle_calculator as gcc

gcc.distance_between_points(p1, p2, unit='kilometers', body=gcc.MARS)

ceres = gcc.CelestialBody('Ceres', radius_meters=470_000)
gcc.distance_between_points(p1, p2, unit='kilometers', body=ceres)
```

For a quick one-off sphere without building a `CelestialBody`, pass `radius=` directly (interpreted in `unit`, and it takes priority over `body` if both are given):

```python
gcc.distance_between_points(p1, p2, planet_radius=1000)
```

`midpoint()` and `intermediate_point()` are calculated without the need for knowing which planet you're on.

 ### Library `compass`
 
 This library was created to let me call, say `Compass.east` so I can get 90deg.  I thought it helped with code readability at first, kept it because it might be useful...   
 
 It has two classes called `CompassSimple` and `CompassComplex`.  `CompassComplex` is still in the todo list, but it contains more information about each compass point.  
 
 To see the eligible points, see [here](https://en.wikipedia.org/wiki/Points_of_the_compass#32_compass_points).  Simply use the terms in "Compass point", use lower case and underscores where there are spaces or dashes.  Alternatively you may use the "Abbreviation" with the appropriate case to call the same value.  
 
 To use `CompassSimple`:
 
 ```python
from great_circle_calculator.compass import CompassSimple as compass

print(compass.east)  # prints 90
print(compass.north)  # prints 0
print(compass.northwest_by_north)  # prints 326.250
print(compass.SEbE)  # Southeast by east, prints 123.750
print(compass.SWbS == compass.southwest_by_south)  # prints True
```

  
 ### Library `_constants`
 
 This was created for two purposes:
 
 1) To easily store the radius of the earth in various units

 2) To have thin wrappers for the trig functions in particular for the arcsin and arctan which have domain limits of -1 to 1, and due to floating point errors, numbers can occationally be outside those domain limits and I didn't want the code crashing about this.

   To see the available units, call `_constants.eligible_units` and a list of the units that are available will be given. 
 
 ###### `eligible_units`
 
 To see the available units, call `_constants.eligible_units` and a list of the units that are available will be given. 

 The `eligible_units` can also have, by default, common aliases and some alternate spellings.  

| Unit | Factor | Alaises |
| --- | --- | --- |
| meters | 1.0 | m, meter, metre, metres |
| kilometers | 1/1000 | km, kilometer, kilometre, kilometres |
| centimeters | 100.0 | cm, centimeter, centimetre, centimetres |
| millimeters | 1000.0 | mm, millimeter, millimetre, millimetres |
| miles | 1/1609.344 | mi, mile |
| feet | 3.28084 | ft, foot |
| inches | 39.3701 | in, inch |
| yards | 1.09361 | yd, yard |
| nautical_miles | 1/1852 | nautical_mile, nauticalmile, nm, nmi, nautical_mile |
| fathoms | 1/1.8288 | ftm, fathom |
| furlongs | 1/201.168 | furlong |

Please note, the nautical mile unit is an international nautical mile.  
 
 ### Libraries  `__conversion` and `__error_checking`
 
Private libraries that convert (`__conversion.py`) values between radians and degrees as the default option for python's math package is radians.  
 
The error checking library (`__error_checking.py`) is used to ensure that the points passed to through the code make sense in the project.  That is, it checks two things.  First, that the point passed to the function is a `tuple` or other Point of length 2. If this check fails, a `TypeError` is thrown.  

The second is that the information contained within the tuple matches the expected range of latitude and longitude. The first element of the `tuple` should be the longitude in the range of [-180, 180] and the second element is the latitude in the range of [-90, 90].  

If this check fails, but it appears that the user has "flipped" the elements of the point (i.e. (lat, lon) is provided), a `ValueError` is thrown with information indicating the belief you have flipped the elements of the coordinates.  If this is not true, `ValueError` is thrown with a different error message indicating the expected input.

Keep in mind that there is a lon-lat lat-lon flipper in the functions.  

 ## And finally...

 Package last updated October 2026.  Readme last updated October 2026.  
 
 ## Change Log

 * 2.1.0 - functions that take a point or return a point now have the parameter `lat_lon`.  Set `lat_lon=True` to pass points in the form `(lat, lon)`. Points that are passed with this `lat_lon=True` will also return their results as `(lat, lon)`
 * 2.0.0 - Big version bump and I wanted to add a bunch of things I wanted to a few years ago plus some other things I've learned since then.  The big thing was allowing custom units and custom radii into the formulas. I corrected a few typos here and there and added some type hints.  I also added units are no longer a fixed list: `register_unit(name, units_per_meter)` lets you add any distance unit, and `eligible_units()` now reflects whatever's registered. Added a `CelestialBody` class plus predefined `EARTH`, `MOON`, `MARS`, `VENUS`, `MERCURY` bodies so `distance_between_points` and `point_given_start_and_bearing` can compute on other planets via `body=`; a one-off custom sphere can also be supplied directly with `planet_radius=`. `intermediate_point` was refactored to compute the central angle directly instead of going through `distance_between_points`/Earth's radius, so it's now body-agnostic by construction. Added type hints throughout (`tuple[float, float]`, PEP 604 unions via `from __future__ import annotations`) targeting Python 3.9+.
 * 1.3.1 - Put in a line of code when computing the haversine distance to ensure that (due to floating point errors) may be above 1
 * 1.3.0 - Updated the code in the `__error_checking.py` file to, by default, throw errors rather than try to correct points. Also expanded the error messages here to be more clear.
 * 1.2.0 - If the user sends a point that is `decimal` data type, it will convert to a tuple of `float` types.  Updated the readme for clarity  
 * 1.1.0 - Changed `haversine=True` as the default for [`distance_between_points`](#function-distance_between_points) as it more accurately reflects the small distance calculation I am using in my projects.
 * 1.0.2 - squished an error in the intermediate function. The number of errors has been embarrassing. I hope you won't judge me too harshly.  
 * 1.0.1.post1 - includes a domain checker for `asin()` and `acos()` because rounding errors can cause the function to be out of range.
 * 1.0.post1 - I screwed up the numbering order, still new at this... please ignore.
 * 1.0.1 - Fixed an error in the [`point_given_start_and_bearing`](#function-point_given_start_and_bearing)
 * 1.0.0 - First Edition, initial commit, etc.
