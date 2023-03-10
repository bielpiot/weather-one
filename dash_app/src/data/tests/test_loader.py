import pytest

@pytest.fixture
def valid_test_dataframe():
    pass

@pytest.fixture
def invalid_test_dataframe():
    pass

def test_load_successful(valid_test_dataframe):
    pass

def test_load_fails_corrupt_data(invalid_test_dataframe):
    pass

def test_load_fails_not_pandas_df():
    pass

