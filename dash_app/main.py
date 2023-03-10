from dash import Dash, html, dcc
from dash_bootstrap_components.themes import BOOTSTRAP
import pandas as pd
import os
from .src.components.layout import create_layout

BUCKET_NAME = os.getenv('BUCKET_NAME')
CSV_NAME = os.getenv('CSV_NAME', 'astro_weather_data.csv')
data = f'{BUCKET_NAME}/{CSV_NAME}'

def main():
    app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
    app.title = 'Weather One'
    app.layout = create_layout(app)

if __name__ == '__main__':
    main()    