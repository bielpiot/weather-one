import pytest
import pandas as pd
from .weather_data_generator import FakeWeatherDataGenerator
from ..loader import DataSchema
from ..source import DataSource
import random

LOCATION_NO = 5
TIMEPOINT_NO = 10

@pytest.fixture
def valid_test_DataSource() -> pd.DataFrame:
    df_coumns = DataSchema.__fields__
    data = FakeWeatherDataGenerator(location_no=LOCATION_NO, timepoint_no=TIMEPOINT_NO).produce_data()
    df = pd.DataFrame(data, columns=df_coumns)
    return DataSource(df)

def test_DataSource_locations_list(valid_test_DataSource):
    assert len(valid_test_DataSource.locations_list) == LOCATION_NO

def test_DataSource_measures_list(valid_test_DataSource):
    measures_list = valid_test_DataSource.measures_list
    assert len(measures_list) == 9
    assert 'location' and 'timepoint' not in measures_list
    assert 'temp2m' and 'seeing' in measures_list

def test_DataSource_row_count(valid_test_DataSource):
    row_count = valid_test_DataSource.row_count
    assert row_count == LOCATION_NO * TIMEPOINT_NO

def test_DataSource_secondary_measures_list(valid_test_DataSource):
    meas_list = valid_test_DataSource.secondary_measures_list
    assert sorted(meas_list) ==  sorted(['cloudcover', 'lifted_index', 'transparency',
                                    'rh2m', 'wind10m_speed'])   

def test_DataSource_filter(valid_test_DataSource):
    measures = ['temp2m', 'transparency', 'lifted_index', 'wind10m_speed']
    random_location = random.choice(valid_test_DataSource.locations_list)
    filtered = valid_test_DataSource.filter(location=random_location, 
                                            measures=measures)
    assert filtered.row_count == 10
    assert filtered.data.shape[1] == 6
    assert sorted(filtered.secondary_measures_list) == sorted(['transparency', 'lifted_index', 'wind10m_speed'])

def test_DataSource_prepare_data_table(valid_test_DataSource):
    assert not valid_test_DataSource.data['timepoint'].is_monotonic_increasing
    assert valid_test_DataSource.build_data_table(sort_by='timepoint')['timepoint'].is_monotonic_increasing 