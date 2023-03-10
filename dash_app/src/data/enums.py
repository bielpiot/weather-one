from enum import Enum

class WindEnum(Enum):
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'
    NORTH_EAST = 'NE'
    NORTH_WEST = 'NW'
    SOUTH_EAST = 'SE'
    SOUTH_WEST = 'SW'

class PrecEnum(Enum):
    RAIN = 'rain'
    SNOW = 'snow'
    FREEZING_RAIN = 'frzr'
    ICE_PELLETS = 'icep'
    NONE = 'none'