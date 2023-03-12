import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from typing import List

from ..data.loader import DataSchema
from ..data.source import DataSource
from . import ids

def render(*, app: Dash, data_source: DataSource) -> html.Div:

    @app.callback(
        Output(ids.LOCATION_DROPDOWN, 'value'),
        Input(ids.MEASURE_DROPDOWN, 'value')
    )
    def select_all_locations(measures: List[str], _: int) -> List[str]:
        return data_source.filter(measures=measures).location_list
    
    return html.Div(
        children = [
            html.H6('Location'),
            dcc.Dropdown(
                id=ids.LOCATION_DROPDOWN,
                options=[
                    {'label': location, "value": location}
                    for location in data_source.locations_list
                ],
                value=data_source.locations_list,
                multi=True,
                placeholder="Select location"

            ),
           html.Button(
                className='dropdown-button',
                children=["Select all"],
                id=ids.SELECT_ALL_LOCATIONS_BUTTON,
                n_clicks=0
           ) 
        ]
    )
