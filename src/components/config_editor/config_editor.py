import dash_bootstrap_components as dbc
from dash import Input, Output, callback, html

from src.app_state import Root
from src.helpers.form import basic_text_input, set_if_valid
from src.helpers.validators import validate_alpha_num, validate_not_blank
from src.model import config as config_factory

from . import item_editor


# ---------------------------------------------------------------------------------------------------
# Name Input
# ---------------------------------------------------------------------------------------------------
def name_input(value: str) -> dbc.Row:
    return basic_text_input(
        "Name",
        "config-name",
        "Enter config name",
        "Name must not be empty and contain only a-z, A-Z, 0-9, and _",
        value,
    )


@callback(
    Output("config-name", "invalid"),
    Input("config-name", "value"),
)
def validate_and_set_name(text: str) -> bool:
    return not set_if_valid(Root.next_config, "name", text, validate_alpha_num)


# ---------------------------------------------------------------------------------------------------
# Description Input
# ---------------------------------------------------------------------------------------------------
def desc_input(value: str) -> dbc.Row:
    return basic_text_input(
        "Description",
        "config-desc",
        "Enter config description",
        "Description must not be empty",
        value,
    )


@callback(
    Output("config-desc", "invalid"),
    Input("config-desc", "value"),
)
def validate_and_set_desc(text: str) -> bool:
    return not set_if_valid(Root.next_config, "desc", text, validate_not_blank)


# ---------------------------------------------------------------------------------------------------
# Save Buttons
# ---------------------------------------------------------------------------------------------------
def save_button() -> html.Div:
    return html.Div(
        className="no-border-toolbar",
        children=[
            dbc.Button(
                " Save",
                id="config-save-button",
                disabled=True,
                className="bi bi-floppy",
            ),
        ],
    )


@callback(
    Output("config-save-button", "disabled"),
    [Input("config-name", "value"), Input("config-desc", "value")],
    prevent_initial_call=True,
)
def needs_save(name: str, desc: str) -> bool:
    if Root.config == Root.next_config:
        return True
    else:
        return False


@callback(
    Output(
        "config-save-button",
        "disabled",
        allow_duplicate=True,
    ),
    Output("config-alert-auto", "is_open"),
    Output("config-alert-error", "is_open"),
    Output("config-alert-error", "children"),
    Input("config-save-button", "n_clicks"),
    prevent_initial_call=True,
)
def save(n_clicks: bool):
    if Root.config_filename is None:
        alert = html.Div(
            [
                html.I(className="bi bi-exclamation-triangle me-2 error-icon"),
                "Config filename not set",
            ]
        )

        return (
            False,
            False,
            True,
            alert,
        )

    if Root.next_config is None:
        alert = html.Div(
            [
                html.I(className="bi bi-exclamation-triangle me-2 error-icon"),
                "Config not loaded",
            ]
        )

        return (
            False,
            False,
            True,
            alert,
        )

    if not Root.next_config.save(Root.config_filename):
        alert = html.Div(
            [html.I(className="bi bi-exclamation-triangle me-2 error-icon")]
            + [
                html.Div(className="error-message", children=error.message)
                for error in Root.next_config.get_errors()
            ]
        )

        return (
            False,
            False,
            True,
            alert,
        )
    else:
        Root.config = Root.next_config.copy()
        return True, True, False, []


# ---------------------------------------------------------------------------------------------------
# Alerts
# ---------------------------------------------------------------------------------------------------
def alerts() -> html.Div:
    return html.Div(
        [
            dbc.Alert(
                [
                    html.I(className="bi bi-check-circle me-2"),
                    f"Schema saved successfully to {Root.config_filename}",
                ],
                id="config-alert-auto",
                is_open=False,
                duration=4000,
            ),
            dbc.Alert(
                [
                    html.I(className="bi bi-exclamation-triangle me-2"),
                    "Error saving Schema",
                ],
                id="config-alert-error",
                is_open=False,
                color="danger",
            ),
            dbc.Alert(
                [
                    html.I(className="bi bi-check-circle me-2"),
                    "Schema exported",
                ],
                id="config-alert-export",
                is_open=False,
                duration=4000,
            ),
        ]
    )


# ---------------------------------------------------------------------------------------------------
# Main Page Layout
# ---------------------------------------------------------------------------------------------------
def layout(fn: str) -> dbc.Form:
    Root.config_filename = fn
    try:
        Root.config = config_factory.load(Root.config_filename)
    except FileNotFoundError:
        return dbc.Form(
            dbc.Alert(
                [
                    html.I(className="bi bi-exclamation-triangle-fill me-2"),
                    f"File {Root.config_filename} does not exist",
                ],
                color="danger",
            )
        )

    Root.next_config = Root.config.copy()

    return dbc.Form(
        [
            html.H2("Config Editor"),
            name_input(Root.next_config.name),
            desc_input(Root.next_config.desc),
            item_editor.layout(),
            html.Br(),
            save_button(),
            html.Br(),
            alerts(),
        ]
    )
