import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, exceptions
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from . import ids
from typing import List
from ..data.source import DataSource
from ..data import mapping as mp

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig

def render(app: Dash, data_source: DataSource) -> html.Div:

    @app.callback(
        Output(ids.LINE_CHART, 'figure'),
        Input(ids.LOCATION_DROPDOWN, 'value'),
        Input(ids.MEASURE_DROPDOWN, 'value'),
    )
    def update_chart(location: str, measures: List[str]) -> go.Figure:
        filtered_data_source = data_source.filter(location=location, measures=measures)
        if not filtered_data_source.row_count:
            return html.Div("No data", id=ids.LINE_CHART)
        data_table = filtered_data_source.build_data_table()
        
        fig = make_subplots(specs=[[{'secondary_y': True}]])

        if 'temp2m' in filtered_data_source.measures_list:
            fig.add_trace(
                go.Scatter(
                    x = data_table['timepoint'],
                    y = data_table['temp2m'],
                    name = 'Temperature',
                    hovertemplate='%{y} °C'
            ))

        for secondary_measure in filtered_data_source.secondary_measures_list:
            hov_text = data_table[f'{secondary_measure}_desc']
            if secondary_measure=='wind10m_speed':
                hov_text = data_table['wind10m_speed_desc'].str.cat(data_table['wind10m_direction'], sep=', direction: ')
            fig.add_trace(
                go.Scatter(
                    x = data_table['timepoint'],
                    y = data_table[secondary_measure],
                    text = hov_text,
                    hovertemplate='%{text}',
                    name=mp.human_readable_measures[secondary_measure]
                ), secondary_y=True,
            )

        fig.update_xaxes(title_text='timepoint')
        min_sec_y = 0
        max_sec_y = 12
        fig.update_yaxes(range=[min_sec_y, max_sec_y], secondary_y=True)
        

        if 'temp2m' in data_table.columns:
            min_y = min(data_table['temp2m']) - 5
            max_y = max(data_table['temp2m']) + 5
            fig.update_yaxes(range=[min_y, max_y], secondary_y=False)
        

        fig.update_layout(legend_itemclick=False, legend_itemdoubleclick=False, hovermode="x")
        fig.update_traces(mode="markers+lines")

        return fig
    
    return html.Div(dcc.Graph(figure=blank_fig(),
                                id=ids.LINE_CHART,
                                className='six columns',
                                config={
                                    'staticPlot': False,
                                    'scrollZoom': True,
                                    'doubleClick': 'reset',
                                    'showTips': True,
                                    'displayModeBar': False,
                                    'watermark': True
                                }))
