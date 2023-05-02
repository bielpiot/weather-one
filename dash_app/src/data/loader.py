from datetime import datetime
from typing import List
import pandas as pd
from pydantic import BaseModel, validator, conint # pylint: disable=no-name-in-module
from . import mapping as mp
from . import fields


class DataSchema(BaseModel):
    """
    Class definition for data schema representation
    """
    location: str
    timepoint: datetime
    cloudcover: conint(ge=fields.Cloudcover.LOW_BOUND, le=fields.Cloudcover.HIGH_BOUND)
    seeing: conint(ge=fields.Seeing.LOW_BOUND, le=fields.Seeing.HIGH_BOUND)
    transparency: conint(
        ge=fields.Transparency.LOW_BOUND, le=fields.Transparency.HIGH_BOUND
    )
    lifted_index: int  # Atmospheric instability, lower = more unstable
    rh2m: conint(ge=fields.Rh2m.LOW_BOUND, le=fields.Rh2m.HIGH_BOUND)
    temp2m: conint(ge=fields.Temp2m.LOW_BOUND, le=fields.Temp2m.HIGH_BOUND)
    prec_type: fields.Prec
    wind10m_direction: fields.WindDirection
    wind10m_speed: conint(ge=fields.WindSpeed.LOW_BOUND, le=fields.WindSpeed.HIGH_BOUND)

    @validator("lifted_index", each_item=True)
    def lifted_index_is_proper(cls: BaseModel, val: int) -> int: # pylint: disable=no-self-argument
        """
        Validator for lifted_index values
        """
        if not val in fields.LiftedIndex.VALUES.value:
            raise ValueError("incorrect lifted index!")
        return val

    @classmethod
    def get_fields_names(cls):
        """
        return list of fields names for DataSchema
        """
        return list(cls.schema().get("properties").keys())


def validate_data_schema(data_schema: BaseModel):
    """
    Decorator to validate input data against provided dataschema
    """

    def wrapper(func):
        class Validator(BaseModel):
            """
            Class providing instance of schema to validate against
            """

            schema_dict: List[data_schema]

        def _wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, pd.DataFrame):
                df_dict = result.to_dict(orient="records")
                _ = Validator(schema_dict=df_dict)
            else:
                raise TypeError("You are not providing pandas.DataFrame")
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
                    raise ValueError(
                        f"Your data has to be unique across columns {columns}"
                    )
            else:
                raise TypeError("You are not providing pandas.DataFrame")
            return result

        return _wrapper

    return wraper


def rescale_data(mapping: List[tuple]):
    """
    Decorator to rescale numeric data - integrity purposes.
    Input list of tuples including column name to be rescaled and dictionary
    with mapping (initial value -> rescaled value)
    """

    def wrapper(func):
        def _wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            for mapper in mapping:
                result.replace({mapper[0]: mapper[1]}, inplace=True)
            return result

        return _wrapper

    return wrapper


def add_descriptions(columns: List[str]):
    """
    Add dolumns with descriptions - utlized later for hovertemplate on chart
    """

    def wrapper(func):
        def _wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            for column in columns:
                mapping = mp.descriptions.get(column)
                desc_column_name = f"{column}_desc"
                result[desc_column_name] = result[column].map(mapping)
            return result

        return _wrapper

    return wrapper


@add_descriptions(
    ["cloudcover", "lifted_index", "seeing", "transparency", "rh2m", "wind10m_speed"]
)
@validate_unique_columns_combinations(["timepoint", "location"])
@rescale_data(
    [("rh2m", mp.RH2M_SCALED_TABLE), ("lifted_index", mp.LIFTED_INDEX_SCALED_TABLE)]
)
@validate_data_schema(DataSchema)
def load_astrometeo_data(path: str) -> pd.DataFrame:
    """
    Loads data from .csv under given path
    """
    data = pd.read_csv(path)
    data["timepoint"] = pd.to_datetime(data["timepoint"])
    return data
