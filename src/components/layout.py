import dash
from dash import Dash, html


def render(app: Dash) -> html.Div:
    return html.Div(
        className="container-fluid",
        children=[
            dash.page_container,
        ],
    )
