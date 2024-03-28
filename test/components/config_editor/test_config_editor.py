import os
from test.mocking.config import MOCK_CONFIG

import dash_bootstrap_components as dbc
from dash import html

from src.app_state import Root
from src.components.config_editor.config_editor import (
    alerts,
    desc_input,
    layout,
    name_input,
    needs_save,
    save,
    save_button,
    validate_and_set_desc,
    validate_and_set_name,
)


def init_valid_config(mock=MOCK_CONFIG):
    Root.config = mock.copy()
    Root.next_config = Root.config.copy()


def test_name_input() -> None:
    assert isinstance(name_input("name"), dbc.Row)


def test_validate_and_set_name_callback() -> None:
    init_valid_config()
    assert not validate_and_set_name("name")
    assert validate_and_set_name("#name#")


def test_desc_input() -> None:
    assert isinstance(desc_input("desc"), dbc.Row)


def test_validate_and_set_desc_callback() -> None:
    init_valid_config()
    assert not validate_and_set_desc("desc")
    assert validate_and_set_desc("")


def test_save_button() -> None:
    assert isinstance(save_button(), html.Div)


def test_needs_save_callback() -> None:
    init_valid_config()
    if Root.next_config is None:
        assert False
    else:
        assert needs_save("name", "desc")
        Root.next_config.name = "new"
        assert not needs_save("name", "desc")


def test_save_callback() -> None:
    init_valid_config()
    if Root.next_config is None:
        assert False
    else:
        Root.config_filename = None
        save_disabled, sucess_alert, error_alert, error_messages = save(True)
        assert not save_disabled
        assert not sucess_alert
        assert error_alert
        assert len(error_messages) == 2

        Root.config_filename = "test/test_config_editor.json"
        assert save(True) == (True, True, False, [])

        Root.next_config.name = ""
        save_disabled, sucess_alert, error_alert, error_messages = save(True)
        assert not save_disabled
        assert not sucess_alert
        assert error_alert
        assert len(error_messages) == 3

        Root.next_config = None
        save_disabled, sucess_alert, error_alert, error_messages = save(True)
        assert not save_disabled
        assert not sucess_alert
        assert error_alert
        assert len(error_messages) == 2


def test_alerts() -> None:
    assert isinstance(alerts(), html.Div)


def test_layout() -> None:
    assert "File missing.json does not exist" in str(layout("missing.json"))
    if not os.path.exists("test/temp"):
        os.mkdir("test/temp")
    CONFIG_FILENAME = "test/temp/config.json"
    MOCK_CONFIG.save(CONFIG_FILENAME)
    assert isinstance(layout(CONFIG_FILENAME), dbc.Form)
