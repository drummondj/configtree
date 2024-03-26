"""A few helpers to clean up form creation"""

import dash_bootstrap_components as dbc


def basic_text_input(
    label: str, attribute: str, placeholder: str, error: str, value: str
) -> dbc.Row:
    """Helper function to create text inputs quickly"""
    return dbc.Row(
        [
            dbc.Label(label, html_for=attribute, width=2),
            dbc.Col(
                children=[
                    dbc.Input(
                        type="text",
                        id=attribute,
                        placeholder=placeholder,
                        value=value,
                    ),
                    dbc.FormFeedback(
                        error,
                        type="invalid",
                    ),
                ],
                width=10,
            ),
        ],
        className="mb-3",
    )
