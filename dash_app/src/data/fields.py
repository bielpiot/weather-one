from enum import Enum, IntEnum

class WindDirection(Enum):
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'
    NORTH_EAST = 'NE'
    NORTH_WEST = 'NW'
    SOUTH_EAST = 'SE'
    SOUTH_WEST = 'SW'

class Prec(Enum):
    RAIN = 'rain'
    SNOW = 'snow'
    FREEZING_RAIN = 'frzr'
    ICE_PELLETS = 'icep'
    NONE = 'none'

class WindSpeed(IntEnum):
    LOW_BOUND = 1
    HIGH_BOUND = 8

class Cloudcover(IntEnum):
    """ lower value = less cloudcover"""
    LOW_BOUND = 1
    HIGH_BOUND = 9

class Seeing(IntEnum):
    """ lower value = better seeing """
    LOW_BOUND = 1
    HIGH_BOUND = 8

class Transparency(IntEnum):
    """ lower value = more transparent """
    LOW_BOUND = 1
    HIGH_BOUND = 8

class Rh2m(IntEnum):
    LOW_BOUND = -4
    HIGH_BOUND = 16

class Temp2m(IntEnum):
    LOW_BOUND = -76
    HIGH_BOUND = 60

class WindSpeed(IntEnum):
    LOW_BOUND = 1
    HIGH_BOUND = 8

class LiftedIndex(Enum):
    VALUES = [-10, -6, -4, -1, 2, 6, 10, 15]