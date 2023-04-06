import pytest
from ..loader import DataSchema, validate_data_schema, validate_unique_columns_combinations, rescale_data
from .weather_data_generator import FakeWeatherDataGenerator
import pandas as pd
import numpy as np
from pydantic import ValidationError
from .. import mapping as mp

@pytest.fixture
def valid_test_dataframe() -> pd.DataFrame:
    df_coumns = DataSchema.__fields__
    data = FakeWeatherDataGenerator().produce_data()
    df = pd.DataFrame(data, columns=df_coumns)
    return df

@pytest.fixture
def invalid_test_dataframe_wrong_types():
    df_coumns = DataSchema.__fields__
    data = FakeWeatherDataGenerator().produce_data()
    data[6] = ['Neverland', 'tomorrow', 1, 4, 'very good', -1, 11, 'much', 1, 'NS', 11]
    df = pd.DataFrame(data, columns=df_coumns)
    return df

@pytest.fixture
def invalid_test_dataframe_values_outide_of_range():
    df_coumns = DataSchema.__fields__
    data = FakeWeatherDataGenerator().produce_data()
    data[4] = ['Jupiter', '2022111106', 11, 11, -33, 0, -2, 151, 'storm', 'NS', 11]
    df = pd.DataFrame(data, columns=df_coumns)
    return df

@pytest.fixture
def invalid_data_not_unique():
    df_columns = DataSchema.__fields__
    data = FakeWeatherDataGenerator().produce_data()
    data[1] = data[2]
    df = pd.DataFrame(data, columns=df_columns)
    return df

@validate_unique_columns_combinations(['timepoint', 'location'])
@validate_data_schema(data_schema=DataSchema)
def digest_df(df: pd.DataFrame) -> pd.DataFrame:
    return df

@rescale_data([('rh2m', mp.RH2M_SCALED_TABLE), ('lifted_index', mp.LIFTED_INDEX_SCALED_TABLE)])
def rescale_df(df:pd.DataFrame) -> pd.DataFrame:
    return df

def test_load_successful(valid_test_dataframe):
    digest_df(valid_test_dataframe)

def test_load_fails_wrong_data(invalid_test_dataframe_wrong_types):
    with pytest.raises(ValidationError):
        digest_df(invalid_test_dataframe_wrong_types)

def test_load_fails_data_out_of_range(invalid_test_dataframe_values_outide_of_range):  
    with pytest.raises(ValidationError):
        digest_df(invalid_test_dataframe_values_outide_of_range)

def test_load_fails_data_not_unique(invalid_data_not_unique):
    with pytest.raises(ValueError):
        digest_df(invalid_data_not_unique)

def test_load_fails_not_pandas_df():
    with pytest.raises(TypeError):
        digest_df('I am not a DataFrame')

def test_df_rescale_successful(valid_test_dataframe):
    df = rescale_df(valid_test_dataframe)
    assert set(df['rh2m'].unique()).issubset(set((mp.RH2M_SCALED_TABLE.values())))
    assert set(df['lifted_index'].unique()).issubset(set((mp.LIFTED_INDEX_SCALED_TABLE.values())))

