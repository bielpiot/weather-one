from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from typing import List
from ..data.mapping import human_readable_measures as hmr

from ..data.source import DataSource
from . import ids

def render(*, app: Dash, data_source: DataSource) -> html.Div:

    @app.callback(
        Output(ids.MEASURE_DROPDOWN, 'value', allow_duplicate=True),
        Input(ids.SELECT_ALL_MEASURES_BUTTON, 'n_clicks'),
        prevent_initial_call=True
    )
    def select_all_measures(_: int) -> List[int]:
        return data_source.graphed_measures_list
    
    @app.callback(
        Output(ids.MEASURE_DROPDOWN, 'value'),
        Input(ids.UNSELECT_ALL_MEASURES_BUTTON, 'n_clicks')
    )
    def deselect_secondary_measures(_: int) -> List:
        return []

    return html.Div(
        children=[
            html.H6("Measure"),
            dcc.Dropdown(
                    id=ids.MEASURE_DROPDOWN,
                    options=[
                        {'label': hmr[measure], 'value': measure}
                        for measure in data_source.graphed_measures_list        
                    ],
                    value=data_source.graphed_measures_list,
                    multi=True,
                    placeholder="Select measures"
            ),
            html.Button(
                className='dropdown-button',
                children=["Select all"],
                id=ids.SELECT_ALL_MEASURES_BUTTON,
                n_clicks=0
            ),
            html.Button(
                className='dropdown-button',
                children=["Unselect all"],
                id=ids.UNSELECT_ALL_MEASURES_BUTTON,
                n_clicks=0
            )
        ]
    )
