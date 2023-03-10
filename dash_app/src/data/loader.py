import pandas as pd
from pydantic import BaseModel, validator, conint
from datetime import datetime
from functools import wraps
from typing import List

from src.data.enums import PrecEnum, WindEnum

class DataSchema(BaseModel):
    location: str
    timepoint: datetime
    cloudcover: conint(ge=1, le=9) # lower = better
    seeing: conint(ge=1, le=8) # lower = better
    tranparency: conint(ge=1, le=8) # lower = better
    lifted_index: int # Atmospheric instability, lower = more unstable
    rh2m: conint(ge=-4, le=16) # relative humidity @ 2m level
    temp2m: conint(ge=-76, le=60)
    prec_type: PrecEnum
    wind10m_direction: WindEnum
    wind10m_speed: conint(ge=1, le=8)

    
    @validator('lifted_index')
    def lifted_index_is_proper(cls, v):
        if not v in [-10, -6, -4, -1, 2, 6, 10, 15]:
            raise ValueError('incorrect lifted index!')
        return v
    
    cloudcover_desc_table = {
                             1: '0%-6%', 2: '6%-19%', 3: '19%-31%', 4: '31%-44%',
                             5: '44%-56%', 6: '56%-69%', 7: '69%-81%', 8: '81%-94%',
                             9: '94%-100%'
                             }
    
    lifted_index_desc_table = {
                               -10: 'Below -7', -6: '-7 to -5', -4: '-5 to -3',
                               -1: '-3 to 0', 2: '0 to 4', 6: '4 to 8',
                               10: '8 to 11', 15: 'Over 11'
                               }
    
    transparency_desc_table = {
                               1: '<0.3', 2: '0.3-0.4', 3: '0.4-0.5',
                               4: '0.5-0.6', 5: '0.6-0.7', 6: '0.7-0.85',
                               7: '0.85-1', 8: '>1'
                               }

    rh2m_desc_table = {**{n: f'{((n+4)*5)}%-{(n+5)*5}%' for n in range(-4,16)},
                       **{16: '100%'}}
    
    wind_desc_table = {
                       1: 'Below 0.3m/s (calm)', 2: '0.3-3.4m/s (light)',
                       3: '3.4-8.0m/s (moderate)', 4: '8.0-10.8m/s (fresh)',
                       5: '10.8-17.2m/s (strong)', 6: '17.2-24.5m/s (gale)',
                       7: '24.5-32.6m/s (storm)', 8: 'Over 32.6m/s (hurricane)'
                       }
    
    secondary_numeric_measures = [cloudcover, seeing, tranparency,
                                   lifted_index, rh2m, wind10m_speed]


def validate_data_schema(data_schema):
    """Decorator to validate a pd.DataFrame against provided data schema"""
    
    @wraps
    def wrapper(func):

        class Validator(BaseModel):
            df_dict: List[data_schema]

        def _wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, pd.DataFrame):
                df_dict = result.to_dict(orient='records')
                _ = Validator(df_dict=df_dict)
            else:
                raise TypeError('You are not providing pandas.DataFrame')
            return result
        
        return _wrapper
    
    return wrapper
                
                
@validate_data_schema(DataSchema)
def load_astrometeo_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    return data

print(DataSchema.__fields__)