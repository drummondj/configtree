from dash import html, callback, Input, Output
import dash_bootstrap_components as dbc
from src.model import schema as schema_factory
from src.helpers.form import basic_text_input
from src.helpers.validators import (
    validate_not_blank,
    validate_alpha_num,
    validate_version_number,
)
from typing import Any, Callable
from . import group_editor
from . import item_editor


# ---------------------------------------------------------------------------------------------------
# Helper Methods
# ---------------------------------------------------------------------------------------------------
def set_if_valid(attribute: str, value: Any, validator: Callable[[Any], bool]) -> bool:
    """Set's a dataclass attribute if valid, returns True if validation passes"""
    if validator(value):
        next_schema.update(attribute, value)
        return True
    else:
        return False


# ---------------------------------------------------------------------------------------------------
# Name Input
# ---------------------------------------------------------------------------------------------------
def name_input(value: str) -> dbc.Row:
    return basic_text_input(
        "Name",
        "name",
        "Enter schema name",
        "Name must not be empty and contain only a-z, A-Z, 0-9, and _",
        value,
    )


@callback(
    Output("name", "invalid"),
    Input("name", "value"),
)
def validate_and_set_name(text: str) -> bool:
    return not set_if_valid("name", text, validate_alpha_num)


# ---------------------------------------------------------------------------------------------------
# Description Input
# ---------------------------------------------------------------------------------------------------
def desc_input(value: str) -> dbc.Row:
    return basic_text_input(
        "Description",
        "desc",
        "Enter schema description",
        "Description must not be empty",
        value,
    )


@callback(
    Output("desc", "invalid"),
    Input("desc", "value"),
)
def validate_and_set_desc(text: str) -> bool:
    return not set_if_valid("desc", text, validate_not_blank)


# ---------------------------------------------------------------------------------------------------
# Version Input
# ---------------------------------------------------------------------------------------------------
def version_input(value: str) -> dbc.Row:
    return basic_text_input(
        "Version",
        "version",
        "Version number in x.y.z format",
        "Version must be in x.y.z format",
        value,
    )


@callback(
    Output("version", "invalid"),
    Input("version", "value"),
)
def validate_and_set_version(text: str) -> bool:
    return not set_if_valid("version", text, validate_version_number)


# ---------------------------------------------------------------------------------------------------
# Save Button
# ---------------------------------------------------------------------------------------------------
def save_button() -> html.Div:
    return html.Div(dbc.Button("Save", id="save-button", disabled=True))


@callback(
    Output("save-button", "disabled"),
    [Input("name", "value"), Input("desc", "value"), Input("version", "value")],
    prevent_initial_call=True,
)
def needs_save(name: str, desc: str, value: str) -> bool:
    global schema, next_schema
    if schema == next_schema:
        return True
    else:
        return False


@callback(
    Output(
        "save-button",
        "disabled",
        allow_duplicate=True,
    ),
    Output("alert-auto", "is_open"),
    Output("alert-error", "is_open"),
    Output("alert-error", "children"),
    Input("save-button", "n_clicks"),
    prevent_initial_call=True,
)
def save(n_clicks: bool):
    global next_schema, schema
    if n_clicks:
        if not next_schema.save(filename):
            return (
                False,
                False,
                True,
                [html.Div(error.message) for error in next_schema.get_errors()],
            )
        else:
            schema = next_schema.copy()
            return True, True, False, []
    else:
        return False, False, False, []


def alerts() -> html.Div:
    return html.Div(
        [
            dbc.Alert(
                f"Schema saved successfully to {filename}",
                id="alert-auto",
                is_open=False,
                duration=4000,
            ),
            dbc.Alert(
                "Error saving Schema",
                id="alert-error",
                is_open=False,
                color="danger",
            ),
        ]
    )


# ---------------------------------------------------------------------------------------------------
# Main Page Layout
# ---------------------------------------------------------------------------------------------------
def layout(fn: str) -> dbc.Form:
    global filename, schema, next_schema
    filename = fn
    try:
        schema = schema_factory.load(filename)
    except FileNotFoundError:
        return dbc.Form(
            dbc.Alert(
                [
                    html.I(className="bi bi-exclamation-triangle-fill me-2"),
                    f"File {filename} does not exist",
                ],
                color="danger",
            )
        )

    next_schema = schema.copy()

    return dbc.Form(
        [
            html.H2("Schema Editor"),
            name_input(next_schema.name),
            desc_input(next_schema.desc),
            version_input(next_schema.version),
            group_editor.layout(next_schema),
            html.Br(),
            item_editor.layout(next_schema),
            html.Br(),
            save_button(),
            html.Br(),
            alerts(),
        ]
    )
