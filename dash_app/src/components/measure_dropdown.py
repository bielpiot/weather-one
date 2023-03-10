from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from typing import List

from ..data.source import DataSource
from . import ids

def render(*, app: Dash, data_source: DataSource) -> html.Div:

    @app.callback(
        Output(ids.MEASURE_DROPDOWN),
        Input(ids.LOCATION_DROPDOWN, 'value'),
        Input(ids.SELECT_ALL_MEASURES_BUTTON, 'n_clicks')
    )
    def select_all_measures(locations: List[str], _: int) -> DataSource:
        return data_source.filter(locations=locations).measures_list


    return html.Div(
        children=[
            html.H6("Measure"),
            dcc.Dropdown(
                    id=ids.MEASURE_DROPDOWN,
                    options=[
                        {'label': measure, 'value': measure}
                        for measure in data_source.measures_list        
                    ],
                    value=data_source.measures_list,
                    multi=True,
                    placeholder="Select measures"
            ),
            html.Button(
                className='dropdown-button',
                children=["Select all"],
                id=ids.SELECT_ALL_MEASURES_BUTTON,
                n_clicks=0
            )
        ]
    )
