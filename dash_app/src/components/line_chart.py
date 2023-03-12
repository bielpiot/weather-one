import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from . import ids
from typing import List
from ..data.source import DataSource

CLOUDCOVER_DESC_TABLE = {
                             1: '0%-6%', 2: '6%-19%', 3: '19%-31%', 4: '31%-44%',
                             5: '44%-56%', 6: '56%-69%', 7: '69%-81%', 8: '81%-94%',
                             9: '94%-100%'
                             }
    
LIFTED_INDEX_DESC_TABLE = {
                            -10: 'Below -7', -6: '-7 to -5', -4: '-5 to -3',
                            -1: '-3 to 0', 2: '0 to 4', 6: '4 to 8',
                            10: '8 to 11', 15: 'Over 11'
                            }

TRANSPARENCY_DESC_TABLE = {
                            1: '<0.3', 2: '0.3-0.4', 3: '0.4-0.5',
                            4: '0.5-0.6', 5: '0.6-0.7', 6: '0.7-0.85',
                            7: '0.85-1', 8: '>1'
                            }

RH2M_DESC_TABLE = {**{n: f'{((n+4)*5)}%-{(n+5)*5}%' for n in range(-4,16)},
                    **{16: '100%'}}

WIND_SPEEC_DESC_TABLE = {
                    1: 'Below 0.3m/s (calm)', 2: '0.3-3.4m/s (light)',
                    3: '3.4-8.0m/s (moderate)', 4: '8.0-10.8m/s (fresh)',
                    5: '10.8-17.2m/s (strong)', 6: '17.2-24.5m/s (gale)',
                    7: '24.5-32.6m/s (storm)', 8: 'Over 32.6m/s (hurricane)'
                    }
    

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
        
        fig = make_subplots(specs=[[{'secondary_y': True}]])

        #temperatures line
        fig.add_trace(
            go.Scatter(
                
            )
        )
        # relative humidity line
        # prec indicatiors 
        # wind bar charts


        # main_fig = px.line(
        #     data_frame=filtered_data_source,
        #     title="Astro weather forecast"
        #     x=DataSchema.timepoint,
        # )

        # wind_fig = px.timeline()

        return html.Div(dcc.Graph(figure=[], id=ids.LINE_CHART))
    
    return html.Div(id=ids.LINE_CHART)