import dash
import dash_bootstrap_components as dbc
from src.components.schema_editor import schema_editor


def layout(filename: str) -> dbc.Form:

    return schema_editor.layout(filename)


dash.register_page(__name__, path_template="/editor/<filename>")
