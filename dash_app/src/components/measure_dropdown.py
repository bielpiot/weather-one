from typing import List, Dict
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from ..data.mapping import human_readable_measures as hrm

from ..data.source import DataSource
from . import ids


def render(*, app: Dash, data_source: DataSource) -> html.Div:
    """
    Renders component
    """

    @app.callback(
        Output(
            ids.MEASURE_DROPDOWN, "value", allow_duplicate=True
        ),  # pylint: disable=unexpected-keyword-arg
        [Input(ids.SELECT_ALL_MEASURES_BUTTON, "n_clicks")],
        prevent_initial_call=True,
    )
    def select_all_measures(_: int) -> List[int]:
        return data_source.graphed_measures_list

    @app.callback(
        Output(ids.MEASURE_DROPDOWN, "value"),
        Input(ids.UNSELECT_ALL_MEASURES_BUTTON, "n_clicks"),
    )
    def deselect_secondary_measures(_: int) -> List:
        return []

    @app.callback(
        Output(ids.MEASURE_DROPDOWN, "options"),
        Input(ids.MAIN_STORE, "data"),
        State(ids.MEASURE_DROPDOWN, "options"),
    )
    def update_measure_dropdown(
        updated_data_source: Dict[str, any], current_options: List[Dict[str, str]]
    ):
        updated_data_source = DataSource(pd.DataFrame.from_dict(updated_data_source))
        updated_options = [
            {"label": hrm.get(measure, measure), "value": measure}
            for measure in updated_data_source.graphed_measures_list
        ]
        if updated_options == current_options:
            raise PreventUpdate
        return updated_options

    return html.Div(
        children=[
            html.H6("Measure"),
            dcc.Dropdown(
                id=ids.MEASURE_DROPDOWN,
                options=[
                    {"label": hrm.get(measure, measure), "value": measure}
                    for measure in data_source.graphed_measures_list
                ],
                value=data_source.graphed_measures_list,
                multi=True,
                placeholder="Select measures",
            ),
            html.Button(
                className="dropdown-button",
                children=["Select all"],
                id=ids.SELECT_ALL_MEASURES_BUTTON,
                n_clicks=0,
            ),
            html.Button(
                className="dropdown-button",
                children=["Unselect all"],
                id=ids.UNSELECT_ALL_MEASURES_BUTTON,
                n_clicks=0,
            ),
        ]
    )
