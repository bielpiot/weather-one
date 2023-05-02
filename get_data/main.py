import os
from datetime import datetime
from typing import NamedTuple, Tuple
import pandas as pd
import requests


class Location(NamedTuple):
    """
    Blueprint definition for location data
    """

    name: str
    latitude: float
    longitude: float


warsaw = Location(name="Warsaw", latitude=21.0122287, longitude=52.2296756)
stalowa_wola = Location(name="Stalowa Wola", latitude=22.053586, longitude=50.5826005)

LOCATIONS = (warsaw, stalowa_wola)
BUCKET_NAME = os.environ.get("BUCKET_NAME")


def get_data(locations: Tuple[Location] = LOCATIONS) -> pd.DataFrame:
    """
    Collects astro meteo forecast data for given list of locations
    """

    def _get_location_data(location: Location) -> pd.DataFrame:
        """
        get data for a single location, single API call
        """
        lon = location.longitude
        lat = location.latitude
        tzshift = 1
        URL = f"http://www.7timer.info/bin/api.pl?lon={lon}&lat={lat}&product=astro&tzshift={tzshift}&output=json"

        # extract and format single location data
        try:
            result = requests.get(url=URL, timeout=10).json()
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err) from err

        startpoint = datetime.strptime(result["init"], "%Y%m%d%H")
        dataseries = result["dataseries"]
        df = pd.DataFrame(dataseries)
        df["location"] = location.name
        df["timepoint"] = startpoint + pd.to_timedelta(
            df["timepoint"].astype(int), unit="H"
        )
        return df

    def _format_df(input_df: pd.DataFrame) -> pd.DataFrame:
        """
        Get desired output format
        """
        output_df = input_df.join(pd.DataFrame(df.pop("wind10m").values.tolist()))
        output_df.rename(
            columns={"direction": "wind10m_direction", "speed": "wind10m_speed"},
            inplace=True,
        )
        output_df = output_df.set_index("location")
        return output_df

    df = pd.concat([_get_location_data(location) for location in locations])
    df = _format_df(df)
    return df


def save_astrometeo_data_to_bucket(request, bucket_name: str = BUCKET_NAME) -> None:
    """
    Loads data from api request into bucket (as .csv)
    """
    df = get_data()
    try:
        df.to_csv(f"gs://{bucket_name}/astro_weather_data.csv")
        msg = "Saved succesfully"
    except Exception as exc:
        msg = exc
    print(msg)
