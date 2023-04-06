import requests
from datetime import datetime
import pandas as pd
from collections import namedtuple
from typing import NamedTuple
from typing import List
import json
import os

class Location(NamedTuple):
    name: str
    latitude: float
    longitude: float


warsaw = Location(name='Warsaw', latitude=21.0122287, longitude=52.2296756)
stalowa_wola = Location(name='Stalowa Wola', latitude=22.053586, longitude=50.5826005)

LOCATIONS = [warsaw, stalowa_wola]



def get_data(locations: List[Location] = LOCATIONS) -> pd.DataFrame:
    """
    Collects astro meteo forecast data for given list of locations
    """

    def _get_location_data(location: Location) -> pd.DataFrame:
        """
        get data for a single location, single API call
        """
        LON = location.longitude
        LAT = location.latitude
        TZSHIFT = 1
        URL = f"http://www.7timer.info/bin/api.pl?lon={LON}&lat={LAT}&product=astro&tzshift={TZSHIFT}&output=json"

        #extract and format single location data
        result = requests.get(URL).json()
        startpoint = datetime.strptime(result['init'], '%Y%m%d%H')
        dataseries = result['dataseries']
        df = pd.DataFrame(dataseries)
        df['location'] = location.name
        df['timepoint'] = startpoint + pd.to_timedelta(df['timepoint'].astype(int), unit='H') 
        return df
    
    def _format_df(input_df: pd.DataFrame) -> pd.DataFrame:
        """
        Get desired output format
        """
        output_df = input_df.join(pd.DataFrame(df.pop('wind10m').values.tolist()))
        output_df.rename(columns={'direction':'wind10m_direction', 'speed':'wind10m_speed'}, inplace=True)
        output_df = output_df.set_index('location')
        return output_df

    df = pd.concat([_get_location_data(location) for location in locations])
    df = _format_df(df)
    return df
    

def load_astrometeo_data_to_bucket(request) -> str:
    request = request.get_data()
    try: 
        request_json = json.loads(request.decode())
    except ValueError as e:
        print(f"Error decoding JSON: {e}")
        return "JSON Error", 400
    df = get_data()
    bucket_name = os.environ.get("BUCKET_NAME")
    df.to_csv(f'gs://{bucket_name}/astro_weather_data.csv')
    msg = "Loaded succesfully"
    print(msg)
    return msg

print(get_data())
    