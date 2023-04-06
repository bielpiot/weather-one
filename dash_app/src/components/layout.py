from dash import Dash, html
from src.components import line_chart, location_dropdown, measure_dropdown, table

from src.data.source import DataSource



def create_layout(*, app: Dash, data_source: DataSource) -> html.Div:
    return html.Div(
        className='app-div',
        children= [
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className='dropdown-container',
                children=[
                    location_dropdown.render(app=app, data_source=data_source),
                    measure_dropdown.render(app=app, data_source=data_source)
                ],
            ),
            table.render(app=app, data_source=data_source),
            line_chart.render(app=app, data_source=data_source)
        ]
    )
    

