from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from ..data.source import DataSource
from . import ids
from typing import List, Dict, Any
from ..data import mapping as mp


def render(*, app: Dash, data_source: DataSource) -> html.Div:
    
    @app.callback(
        Output(ids.TABLE, 'children'),
        Input(ids.LINE_CHART, 'hoverData'),
        Input(ids.MEASURE_DROPDOWN, 'value'),
        Input(ids.LOCATION_DROPDOWN, 'value')
    )
    def build_table(hov_data: Dict[str, Any], measures: List[str], location: str):
        df = DataSource.filter(location=location, measures=measures)

        timer = dcc.Interval()


        current_timepoint = df['timepoint'].min()
        if hov_data is None: 
            highlight_timepoint = current_timepoint
        else:
            highlight_timepoint = hov_data['timepoint']
        data_snapshot = df[df['timestamp'] == highlight_timepoint]
        
        measures_markdown_part = '\n'.join([f'{measure}' for measure in df.measures])
        weather_symbol = 'placeholder'

        table = dcc.Markdown(
            f"""
            {data_snapshot}
            {measures_markdown_part}
            {weather_symbol}
            """
            )
        
        return table
        