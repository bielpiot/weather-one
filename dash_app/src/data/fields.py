"""Fields definition for DataSchema used"""
from enum import Enum, IntEnum


class WindDirection(Enum):
    """
    Wind direction data field representation
    """
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    NORTH_EAST = "NE"
    NORTH_WEST = "NW"
    SOUTH_EAST = "SE"
    SOUTH_WEST = "SW"


class Prec(Enum):
    """
    Precipitation type data field representation
    """
    RAIN = "rain"
    SNOW = "snow"
    FREEZING_RAIN = "frzr"
    ICE_PELLETS = "icep"
    NONE = "none"


class WindSpeed(IntEnum):
    """
    Wind speed data field representation
    """
    LOW_BOUND = 1
    HIGH_BOUND = 8


class Cloudcover(IntEnum):
    """
    Cloud cover data field representation
    Lower value = less cloud cover
    """

    LOW_BOUND = 1
    HIGH_BOUND = 9


class Seeing(IntEnum):
    """
    Astronomical seeing data field representation
    Lower value = better seeing
    """

    LOW_BOUND = 1
    HIGH_BOUND = 8


class Transparency(IntEnum):
    """
    Atmosphere transparency data field representation
    Lower value = more transparency
    """

    LOW_BOUND = 1
    HIGH_BOUND = 8


class Rh2m(IntEnum):
    """
    Relative humidity data field representation
    """
    LOW_BOUND = -4
    HIGH_BOUND = 16


class Temp2m(IntEnum):
    """
    Temperature data field representation
    """
    LOW_BOUND = -76
    HIGH_BOUND = 60


class LiftedIndex(Enum):
    """
    Atmosphere stability data field representation; in practice represents chance of storm possibility
    Lower value = more unstable
    """
    VALUES = [-10, -6, -4, -1, 2, 6, 10, 15]
