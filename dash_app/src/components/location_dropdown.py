from dash import Dash, dcc, html
from ..data.source import DataSource
from . import ids


def render(*, app: Dash, data_source: DataSource) -> html.Div: # pylint: disable=unused-argument
    """
    Renders component
    """
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
