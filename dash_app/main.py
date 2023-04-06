from dash import Dash, html, dcc
import os
from .src.components.layout import create_layout
from .src.data.source import DataSource
from .src.data.loader import load_astrometeo_data

BUCKET_NAME = os.getenv('BUCKET_NAME')
CSV_NAME = os.getenv('CSV_NAME', 'astro_weather_data.csv')

data_path = f'{BUCKET_NAME}/{CSV_NAME}'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def main(path: str) -> None:
    data = load_astrometeo_data(path)
    data = DataSource(data)

    app = Dash(__name__, external_stylesheets=external_stylesheets)
    app.title = 'Weather One'
    app.layout = create_layout(app=app, data_source=data)
    app.run()

if __name__ == '__main__':
    main(path=data_path)   