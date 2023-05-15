import datetime
import pandas as pd
from typing import Dict, Any
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from ..data.source import DataSource
from . import ids


def render(*, app: Dash) -> html.Div:
    """
    Renders component
    """

    @app.callback(
        Output(ids.TIME_STORE, "data"), Input(ids.INTERVAL_COMPONENT, "n_intervals")
    )
    def update_and_store_timestamp(_: int) -> datetime.datetime:
        return datetime.datetime.now()

    @app.callback(
        Output(ids.TABLE, "children"),
        [
            Input(ids.LINE_CHART, "hoverData"),
            Input(ids.LOCATION_DROPDOWN, "value"),
            Input(ids.TIME_STORE, "data"),
        ],
        State(ids.MAIN_STORE, "data"),
    )
    def build_table(
        hov_data: Dict[str, Any],
        location: str,
        timepoint: datetime.datetime,
        data_source: Dict[str, any],
    ) -> dcc.Markdown:
        data_source = DataSource(pd.DataFrame.from_dict(data_source))
        df = data_source.filter(location=location, measures=None)
        df = df.build_data_table()

        current_timepoint = df[df["timepoint"] < timepoint]["timepoint"].iloc[0]
        if hov_data is None:
            highlight_timepoint = current_timepoint
        else:
            highlight_timepoint = hov_data["points"][0]["x"]
        highlight_timepoint = str(highlight_timepoint)
        data_snapshot = df[df["timepoint"] == highlight_timepoint].to_dict("records")[0]

        table = html.Div(
            children=[
                dcc.Markdown(
                    f"""
            ## {datetime.datetime.strftime(data_snapshot['timepoint'], "%d %b %Y, %I %p")}\n"""
                ),
                dcc.Markdown(
                    f"""
            Temp: {data_snapshot['temp2m']}\n
            Wind : {data_snapshot['wind10m_speed']} m/s | {data_snapshot['wind10m_direction']}\n
            Precipitation : {data_snapshot['prec_type'] if data_snapshot['prec_type'] != "none" else "clear"}\n
            Transparency: {data_snapshot['transparency_desc']}\n
            Seeing : {data_snapshot['seeing_desc']}\n
            Cloud coverage: {data_snapshot['cloudcover_desc']}\n
            Relative humidity : {data_snapshot['rh2m_desc']}\n***
            """
                ),
            ]
        )

        return table

    return html.Div(
        [
            dcc.Interval(id=ids.INTERVAL_COMPONENT, interval=60 * 1000, n_intervals=0),
            dcc.Store(id=ids.TIME_STORE, data=datetime.datetime.now()),
            html.Div(id=ids.TABLE),
        ]
    )
