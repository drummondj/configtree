import tkinter as tk
from tkinter import filedialog

import dash_bootstrap_components as dbc
from dash import Input, Output, callback, html

from src.app_state import Root
from src.helpers.form import basic_text_input, set_if_valid
from src.helpers.validators import (
    validate_alpha_num,
    validate_not_blank,
    validate_version_number,
)
from src.model import config as config_factory
from src.model import schema as schema_factory

from . import group_editor, item_editor


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
    return not set_if_valid(Root.next_schema, "name", text, validate_alpha_num)


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
    return not set_if_valid(Root.next_schema, "desc", text, validate_not_blank)


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
    return not set_if_valid(Root.next_schema, "version", text, validate_version_number)


# ---------------------------------------------------------------------------------------------------
# Save & Export Buttons
# ---------------------------------------------------------------------------------------------------
def save_button() -> html.Div:
    return html.Div(
        className="no-border-toolbar",
        children=[
            dbc.Button(
                " Save", id="save-button", disabled=True, className="bi bi-floppy"
            ),
            dbc.Button(
                " Export Config",
                id="export-config-button",
                className="bi bi-arrow-right-square",
                color="dark",
                outline=True,
            ),
        ],
    )


@callback(
    Output("save-button", "disabled"),
    [Input("name", "value"), Input("desc", "value"), Input("version", "value")],
    prevent_initial_call=True,
)
def needs_save(name: str, desc: str, value: str) -> bool:
    if Root.schema == Root.next_schema:
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
    if Root.schema_filename is None:
        alert = html.Div(
            [
                html.I(className="bi bi-exclamation-triangle me-2 error-icon"),
                "Schema filename not set",
            ]
        )

        return (
            False,
            False,
            True,
            alert,
        )

    if Root.next_schema is None:
        alert = html.Div(
            [
                html.I(className="bi bi-exclamation-triangle me-2 error-icon"),
                "Schema not loaded",
            ]
        )

        return (
            False,
            False,
            True,
            alert,
        )

    if not Root.next_schema.save(Root.schema_filename):
        alert = html.Div(
            [html.I(className="bi bi-exclamation-triangle me-2 error-icon")]
            + [
                html.Div(className="error-message", children=error.message)
                for error in Root.next_schema.get_errors()
            ]
        )

        return (
            False,
            False,
            True,
            alert,
        )
    else:
        Root.schema = Root.next_schema.copy()
        return True, True, False, []


@callback(Output("export-config-button", "disabled"), Input("save-button", "disabled"))
def disable_export_config_button(save_button_state: bool):
    return not save_button_state


@callback(
    Output("alert-export", "is_open"),
    Input("export-config-button", "n_clicks"),
    prevent_initial_call=True,
)
def click_export_config_button(n_clicks: int):
    if Root.schema_filename is not None:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        filename = filedialog.asksaveasfilename()

        if filename:
            Root.config = config_factory.Config(
                "untitiled", "Insert description here", Root.schema_filename
            )
            Root.config.generate_items()
            Root.config_filename = filename
            Root.next_config = Root.config.copy()
            Root.next_config.save(Root.config_filename)

        return True
    return False


# ---------------------------------------------------------------------------------------------------
# Alerts
# ---------------------------------------------------------------------------------------------------
def alerts() -> html.Div:
    return html.Div(
        [
            dbc.Alert(
                [
                    html.I(className="bi bi-check-circle me-2"),
                    f"Schema saved successfully to {Root.schema_filename}",
                ],
                id="alert-auto",
                is_open=False,
                duration=4000,
            ),
            dbc.Alert(
                [
                    html.I(className="bi bi-exclamation-triangle me-2"),
                    "Error saving Schema",
                ],
                id="alert-error",
                is_open=False,
                color="danger",
            ),
            dbc.Alert(
                [
                    html.I(className="bi bi-check-circle me-2"),
                    "Schema exported",
                ],
                id="alert-export",
                is_open=False,
                duration=4000,
            ),
        ]
    )


# ---------------------------------------------------------------------------------------------------
# Main Page Layout
# ---------------------------------------------------------------------------------------------------
def layout(fn: str) -> dbc.Form:
    Root.schema_filename = fn
    try:
        Root.schema = schema_factory.load(Root.schema_filename)
    except FileNotFoundError:
        return dbc.Form(
            dbc.Alert(
                [
                    html.I(className="bi bi-exclamation-triangle-fill me-2"),
                    f"File {Root.schema_filename} does not exist",
                ],
                color="danger",
            )
        )

    Root.next_schema = Root.schema.copy()

    return dbc.Form(
        [
            html.H2("Schema Editor"),
            name_input(Root.next_schema.name),
            desc_input(Root.next_schema.desc),
            version_input(Root.next_schema.version),
            group_editor.layout(),
            html.Br(),
            item_editor.layout(Root.next_schema),
            html.Br(),
            save_button(),
            html.Br(),
            alerts(),
        ]
    )
