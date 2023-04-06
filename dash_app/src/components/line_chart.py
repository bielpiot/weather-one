import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from . import ids
from typing import List
from ..data.source import DataSource
from ..data import mapping as mp


def render(app: Dash, data_source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.LINE_CHART, 'figure'),
        Input(ids.LOCATION_DROPDOWN, 'value'),
        Input(ids.MEASURE_DROPDOWN, 'value'),
    )
    def update_chart(locations: List[str], measures: List[str]) -> go.Figure:
        filtered_data_source = data_source.filter(locations=locations, measures=measures)
        if not filtered_data_source.row_count:
            return html.Div("No data", id=ids.LINE_CHART)
        data_table = filtered_data_source.build_data_table()
        
        fig = make_subplots(specs=[[{'secondary_y': True}]])
        

        if 'temp2m' in filtered_data_source.measures_list:
        #temperatures line
            fig.add_trace(
                go.Scatter(
                    x = data_table['timepoint'],
                    y = data_table['temp2m'],
                    name = 'temperature'
                ), secondary_y=False,
            )

        # relative humidity line
        # prec indicatiors
        for secondary_measure in filtered_data_source.secondary_measures_list:
            fig.add_trace(
                go.Scatter(
                    x = data_table['timepoint'],
                    y = data_table[secondary_measure]
                ), secondary_y=True,
            )

        min_y = min(data_table['temp2m']) - 5
        max_y = max(data_table['temp2m']) + 5
        min_sec_y = 0
        max_sec_y = 12

        fig.update_yaxes(range=[min_sec_y, max_sec_y], secondary_y=True, title_text='temp')
        fig.update_yaxes(range=[min_y, max_y], secondary_y=False)
        fig.update_xaxes(title_text='timepoint')

        return fig

    return html.Div(dcc.Graph(figure=[],
                                id=ids.LINE_CHART,
                                className='six columns',
                                config={
                                    'staticPlot': False,
                                    'scrollZoom': True,
                                    'doubleClick': 'reset',
                                    'showTips': True,
                                    'displayModeBar': 'hover',
                                    'watermark': True
                                }))
