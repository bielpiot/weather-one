from dash import Dash, html
import dash_bootstrap_components as dbc
from . import (
    line_chart,
    location_dropdown,
    measure_dropdown,
    table,
)

from ..data.source import DataSource


def create_layout(*, app: Dash, data_source: DataSource) -> html.Div:
    """
    Creates app layout
    """
    return html.Div(
        [
            html.H1(app.title),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            location_dropdown.render(app=app, data_source=data_source)
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        html.Div(
                            measure_dropdown.render(app=app, data_source=data_source)
                        ),
                        width=8,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(table.render(app=app, data_source=data_source)),
                        width=3,
                    ),
                    dbc.Col(
                        html.Div(line_chart.render(app=app, data_source=data_source)),
                        width=9,
                    ),
                ]
            ),
        ],
        className="app-div",
    )
