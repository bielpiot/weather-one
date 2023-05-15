import os
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from . import (
    line_chart,
    location_dropdown,
    measure_dropdown,
    table,
    ids,
)

from ..data.source import DataSource
from ..data.loader import load_astrometeo_data

BUCKET_NAME = os.getenv("BUCKET_NAME")
CSV_NAME = os.getenv("CSV_NAME", "astro_weather_data.csv")
FAILSAFE_CSV_NAME = os.getenv("FAILSAFE_CSV_NAME", "failsafe_data.csv")


def create_layout(*, app: Dash) -> html.Div:
    """
    Creates app layout
    """

    def _update_data():
        data_path = f"gs://{BUCKET_NAME}/{CSV_NAME}"
        failsafe_data_path = f"gs://{BUCKET_NAME}/{FAILSAFE_CSV_NAME}"
        data = load_astrometeo_data(path=data_path, failsafe_path=failsafe_data_path)
        data_source = DataSource(data)
        return data_source

    data_source = _update_data()

    @app.callback(
        Output(ids.MAIN_STORE, "data"), Input(ids.MAIN_INTERVAL, "n_intervals")
    )
    def update_data(_: int) -> DataSource:
        return _update_data().data.to_dict()

    return html.Div(
        [
            dcc.Interval(id=ids.MAIN_INTERVAL, interval=3600 * 1000, n_intervals=0),
            dcc.Store(
                id=ids.MAIN_STORE,
                data=data_source.data.to_dict(),
            ),
            html.Div(
                [
                    html.H1(app.title),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    location_dropdown.render(
                                        app=app, data_source=data_source
                                    )
                                ),
                                width=4,
                            ),
                            dbc.Col(
                                html.Div(
                                    measure_dropdown.render(
                                        app=app, data_source=data_source
                                    )
                                ),
                                width=8,
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(table.render(app=app)),
                                width=3,
                            ),
                            dbc.Col(
                                html.Div(line_chart.render(app=app)),
                                width=9,
                            ),
                        ]
                    ),
                ],
                className="app-div",
                id=ids.MAIN,
            ),
        ]
    )
