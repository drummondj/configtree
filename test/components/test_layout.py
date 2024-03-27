from src.components.layout import render
from dash import Dash, html
import dash_bootstrap_components as dbc


def test_render():
    app = Dash(
        external_stylesheets=[
            "./assets/stle.css",
            dbc.themes.BOOTSTRAP,
            dbc.icons.BOOTSTRAP,
        ],
        suppress_callback_exceptions=True,
    )
    app.title = "ConfigTree"
    app.layout = render(
        app,
    )
    assert isinstance(app.layout, html.Div)
