import os
from dash import Dash
import dash_bootstrap_components as dbc
from src.components.layout import create_layout
from src.data.source import DataSource
from src.data.loader import load_astrometeo_data

BUCKET_NAME = os.getenv("BUCKET_NAME")
CSV_NAME = os.getenv("CSV_NAME", "astro_weather_data.csv")
FAILSAFE_CSV_NAME = os.getenv("FAILSAFE_CSV_NAME", "failsafe_data.csv")

data_path = f"gs://{BUCKET_NAME}/{CSV_NAME}"
failsafe_data_path = f"gs://{BUCKET_NAME}/{FAILSAFE_CSV_NAME}"
external_stylesheets = [dbc.themes.SLATE]
data = load_astrometeo_data(path=data_path, failsafe_path=failsafe_data_path)
data = DataSource(data)

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Weather One"
app.layout = create_layout(app=app, data_source=data)
server = app.server

if __name__ == "__main__":
    app.run(debug=False)
