from typing import List, Dict
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from ..data.source import DataSource
from . import ids


def render(*, app: Dash, data_source: DataSource) -> html.Div:
    """
    Renders component
    """

    @app.callback(
        Output(ids.LOCATION_DROPDOWN, "options"),
        Input(ids.MAIN_STORE, "data"),
        State(ids.LOCATION_DROPDOWN, "options"),
    )
    def update_dropdown(
        updated_data_source: Dict[str, any], current_data_options: List[Dict[str, str]]
    ):
        updated_data_source = DataSource(pd.DataFrame.from_dict(updated_data_source))
        updated_data_options = [
            {"label": location, "value": location}
            for location in updated_data_source.locations_list
        ]
        if updated_data_options == current_data_options:
            raise PreventUpdate
        return updated_data_options

    return html.Div(
        children=[
            html.H6("Location"),
            dcc.Dropdown(
                id=ids.LOCATION_DROPDOWN,
                options=[
                    {"label": location, "value": location}
                    for location in data_source.locations_list
                ],
                value=data_source.locations_list[0],
                multi=False,
                clearable=False,
                placeholder="Select location",
            ),
        ]
    )
