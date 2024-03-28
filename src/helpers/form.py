"""A few helpers to clean up form creation"""

from typing import Any, Callable

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


def set_if_valid(
    object: object, attribute: str, value: Any, validator: Callable[[Any], bool]
) -> bool:
    """Set's a dataclass attribute if valid, returns True if validation passes"""

    if validator(value):
        setattr(object, attribute, value)
        return True
    else:
        return False
