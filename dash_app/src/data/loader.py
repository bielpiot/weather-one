import pandas as pd
from pydantic import BaseModel, validator, conint, root_validator
from datetime import datetime
from functools import wraps
from typing import List

import dash_app.src.data.fields as fields

class DataSchema(BaseModel):
    location: str
    timepoint: datetime
    cloudcover: conint(ge=fields.Cloudcover.LOW_BOUND, le=fields.Cloudcover.HIGH_BOUND) 
    seeing: conint(ge=fields.Seeing.LOW_BOUND, le=fields.Seeing.HIGH_BOUND) 
    tranparency: conint(ge=fields.Transparency.LOW_BOUND, le=fields.Transparency.HIGH_BOUND) 
    lifted_index: int # Atmospheric instability, lower = more unstable
    rh2m: conint(ge=fields.Rh2m.LOW_BOUND, le=fields.Rh2m.HIGH_BOUND) 
    temp2m: conint(ge=fields.Temp2m.LOW_BOUND, le=fields.Temp2m.HIGH_BOUND) 
    prec_type: fields.Prec
    wind10m_direction: fields.WindDirection
    wind10m_speed: conint(ge=fields.WindSpeed.LOW_BOUND, le=fields.WindSpeed.HIGH_BOUND) 

    
    @validator('lifted_index', each_item=True)
    def lifted_index_is_proper(cls: BaseModel, v: int) -> int:
        if not v in fields.LiftedIndex.VALUES.value:
            raise ValueError('incorrect lifted index!')
        return v
        


def validate_data_schema(data_schema: BaseModel):
    """
    Decorator to validate input data against provided dataschema
    """
    
    # @wraps
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


def validate_unique_columns_combinations(columns: List[str]):
    """
    Decorator to check uniqueness of data across columns
    """
    def wraper(func):
        def _wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, pd.DataFrame):
                if any(result.duplicated(subset=[*columns])):
                    raise ValueError(f'Your data has to be unique across columns {columns}')
            else:
                raise TypeError('You are not providing pandas.DataFrame')
            return result
        
        return _wrapper
    return wraper
                
                
@validate_unique_columns_combinations(['timepoint', 'location'])                
@validate_data_schema(DataSchema)
def load_astrometeo_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    return data