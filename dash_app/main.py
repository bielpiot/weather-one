from dash import Dash

import dash_bootstrap_components as dbc
from src.components.layout import create_layout


external_stylesheets = [dbc.themes.SLATE]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Weather One"
app.layout = create_layout(app=app)
server = app.server

if __name__ == "__main__":
    app.run(debug=False)
