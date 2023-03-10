import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from . import ids
from typing import List
from ..data.source import DataSource
from ..data.loader import DataSchema

def render(app: Dash, data_source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.LINE_CHART, 'children'),
        Input(ids.LOCATION_DROPDOWN, 'value'),
        Input(ids.MEASURE_DROPDOWN, 'value'),
    )
    def update_chart(locations: List[str], measures: List[str]) -> html.Div:
        filtered_data_source = data_source.filter(locations=locations, measures=measures)
        if not filtered_data_source.row_count:
            return html.Div("No data", id=ids.LINE_CHART)
        
        fig =make_subplots(specs=[[{'secondary_y': True}]])

        #temperatures lines
        fig.add_trace(
            go.Scatter()
        )

        main_fig = px.line(
            data_frame=filtered_data_source,
            title="Astro weather forecast"
            x=DataSchema.timepoint,

        )

        wind_fig = px.timeline()

        return html.Div(dcc.Graph(figure=[], id=ids.LINE_CHART))
    
    return html.Div(id=ids.LINE_CHART)