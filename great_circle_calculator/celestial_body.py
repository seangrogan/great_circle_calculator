# ---------------------------------------------------------------------------
# Celestial bodies
# ---------------------------------------------------------------------------
from functools import total_ordering

from great_circle_calculator._constants import convert_from_meters
from dataclasses import dataclass

@dataclass(frozen=True)
@total_ordering
class CelestialBody:
    """
    A sphere to run great-circle math on.
    Construct your own for any celestial body not predefined below, e.g.::
    CERES = CelestialBody("Ceres", radius_meters=470_000)
    """
    name: str
    radius_meters: float

    def radius(self, unit: str = "meters") -> float:
        """Returns this body's radius in the requested unit."""
        return convert_from_meters(self.radius_meters, unit)

    def __repr__(self) -> str:
        return f"CelestialBody(name={self.name!r}, radius_meters={self.radius_meters!r})"

    def __str__(self) -> str:
        return f"CelestialBody(name={self.name}, radius_meters={self.radius_meters})"

    def __int__(self):
        return int(self.radius_meters)

    def __float__(self):
        return float(self.radius_meters)

    def __eq__(self, other):
        if isinstance(other, CelestialBody):
            return self.radius_meters == other.radius_meters
        if isinstance(other, int) or isinstance(other, float):
            return self.radius_meters == other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, CelestialBody):
            return self.radius_meters < other.radius_meters
        if isinstance(other, int) or isinstance(other, float):
            return self.radius_meters < other
        return NotImplemented




# FAI sphere. Swap for 6_378_137 (WGS84/Google-Earth equatorial radius) if your use case needs it,
# e.g. `EARTH = CelestialBody("Earth", 6_378_137)`.
EARTH = CelestialBody("Earth", 6_371_000)
MOON = CelestialBody("Moon", 1_737_400)

SOL = CelestialBody("Sol", 695_500_000)
MERCURY = CelestialBody("Mercury", 2_439_700)
VENUS = CelestialBody("Venus", 6_051_800)
MARS = CelestialBody("Mars", 3_389_500)
JUPITER = CelestialBody("Jupiter", 69_886_000)
SATURN = CelestialBody("Saturn", 58_232_000)
URANUS = CelestialBody("Uranus", 25_362_000)
NEPTUNE = CelestialBody("Neptune", 24_622_000)

GANYMEDE = CelestialBody("Ganymede", 2_634_100)


