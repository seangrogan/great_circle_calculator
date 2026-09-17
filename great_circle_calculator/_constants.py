from __future__ import annotations

import math
import warnings
from typing import Iterable

pi = math.pi


# ---------------------------------------------------------------------------
# Trig helpers : wrappers so the rest of the package doesn't need math.*
# everywhere, and so asin/acos are protected from floating-point domain errors.
# The domain checking errors was the large reason for these thin wrappers...
# ---------------------------------------------------------------------------

def sin(x: float) -> float:
    return math.sin(x)


def cos(x: float) -> float:
    return math.cos(x)


def asin(x: float) -> float:
    return math.asin(_clamp_domain(x))


def acos(x: float) -> float:
    return math.acos(_clamp_domain(x))


def atan2(y: float, x: float) -> float:
    return math.atan2(y, x)


def sqrt(x: float) -> float:
    return math.sqrt(x)


def _clamp_domain(x: float, *, eps=0.01, domain_lb=-1, domain_ub=1) -> float:
    """asin/acos are only defined on [-1, 1]. Floating-point error can push an
    otherwise-valid input a hair outside that range, so clamp instead of raising.
    :param x: a value to check and correct if a number should be inside the domain
    :param eps: Epsilon ε a precision value.  If the value exceeds 1 or -1 by this
    amount, let the program through a possible domain error.  this exists to allow
    egregious values to continue to raise an error"""
    if eps is not None and abs(x) - 1.0 > eps:
        return x
    if x > domain_ub:
        warnings.warn(f"Possibly due to floating point errors, the value passed exceeds the "
                      f"domain of [-1, 1]. We are setting the value of {x} to 1", UserWarning)
        return 1.0
    if x < domain_lb:
        warnings.warn(f"Possibly due to floating point errors, the value passed exceeds the "
                      f"domain of [-1, 1]. We are setting the value of {x} to -1", UserWarning)
        return -1.0
    return x


# --------------
# Units
# --------------

# Canonical unit name -> "how many of this unit equal one meter".
# A reasonably complete default set is provided; add your own with register_unit().
_UNITS_PER_METER: dict[str, float] = {
    "meters": 1.0,
    "kilometers": 1 / 1_000,
    "centimeters": 100.0,
    "millimeters": 1_000.0,
    "miles": 1 / 1609.344,
    "feet": 3.28084,
    "inches": 39.3701,
    "yards": 1.09361,
    "nautical_miles": 1 / 1852,
    "fathoms": 1 / 1.8288,
    "furlongs": 1 / 201.168,
    "sean": 1.42016146628846 # my average walking stride length based on the Garmin
}

# I think this is a reasonable amount of aliases for this package
_UNIT_ALIASES_TABLE = {
    "meters": ("m", "meter", "metre", "metres"),
    "kilometers": ("km", "kilometer", "kilometre", "kilometres"),
    "centimeters": ("cm", "centimeter", "centimetre", "centimetres"),
    "millimeters": ("mm", "millimeter", "millimetre", "millimetres"),
    "miles": ("mi", "mile"),
    "feet": ("ft", "foot"),
    "inches": ("in", "inch"),
    "yards": ("yd", "yard"),
    "nautical_miles": ("nautical_mile", "nauticalmile", "nm", "nmi", "nautical_mile"),
    "fathoms": ("ftm", "fathom"),
    "furlongs": ("furlong",),
    "sean": ("sean_steps",)
}
# alias (lowercase) -> canonical unit name.
_UNIT_ALIASES: dict[str, str] = {_k: _v for _v, _l in _UNIT_ALIASES_TABLE.items() for _k in _l}


def register_unit(
    name: str,
    units_per_meter: float,
    *,
    aliases: Iterable[str] = (),
    overwrite: bool = False,
) -> None:
    """Registers a custom distance unit so it can be used anywhere a 'unit=' argument
    is accepted, e.g. 'distance_between_points(p1, p2, unit='metric_foot').

    :param name: the unit's canonical name, e.g. 'metric_foot'
    :param units_per_meter: how many of this unit equal one meter (e.g. 0.3 for metric_foot)
    :param aliases: alternate names that should also resolve to this unit, e.g. ('metric_feet',).
        Matching is case-insensitive.
    :param overwrite: set True to replace an already-registered unit/alias of the same name
    """
    key = name.strip().lower()
    if not overwrite and key in _UNITS_PER_METER:
        raise ValueError(f"Unit '{name}' is already registered. Pass overwrite=True to replace it.")
    if units_per_meter <= 0:
        raise ValueError("units_per_meter must be a positive number")
    _UNITS_PER_METER[key] = units_per_meter
    if isinstance(aliases, str):
        aliases = (aliases,)
    for alias in aliases:
        alias_key = alias.strip().lower()
        if not overwrite and alias_key in _UNIT_ALIASES and _UNIT_ALIASES[alias_key] != key:
            raise ValueError(
                f"Alias '{alias}' is already registered for unit "
                f"'{_UNIT_ALIASES[alias_key]}'. Pass overwrite=True to replace it."
            )
        _UNIT_ALIASES[alias_key] = key


def eligible_units() -> list[str]:
    """Returns the currently-registered canonical unit names (not aliases)."""
    return sorted(_UNITS_PER_METER)


def unit_aliases(name: str) -> list[str]:
    """Returns the known aliases for a canonical unit name, e.g. unit_aliases('meters') -> ['m', 'metre', ...]."""
    canonical = resolve_unit(name)
    return sorted(alias for alias, target in _UNIT_ALIASES.items() if target == canonical)


def resolve_unit(unit: str) -> str:
    """Resolves a unit name or alias to its canonical name, raising ValueError if unrecognized."""
    key = unit.strip().lower()
    if key in _UNITS_PER_METER:
        return key
    if key in _UNIT_ALIASES:
        return _UNIT_ALIASES[key]
    raise ValueError(f"Unit '{unit}' is not recognized. Eligible units: {eligible_units()}")


def _unit_factor(unit: str) -> float:
    return _UNITS_PER_METER[resolve_unit(unit)]


def convert_from_meters(value_m: float, unit: str) -> float:
    """Converts a value in meters into 'unit' (a canonical name or a recognized alias)."""
    return value_m * _unit_factor(unit)


def convert_to_meters(value: float, unit: str) -> float:
    """Converts a value in 'unit' (a canonical name or a recognized alias) into meters."""
    return value / _unit_factor(unit)