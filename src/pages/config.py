import dash
import dash_bootstrap_components as dbc
from src.components.config_editor import config_editor


def layout(filename: str) -> dbc.Form:
    return config_editor.layout(filename)


dash.register_page(__name__, path_template="/config/<filename>")
