from test.mocking.schema import MOCK_SCHEMA, MOCK_SCHEMA_WITH_GROUPS_AND_ITEMS

from dash import html

from src.app_state import Root
from src.components.schema_editor.group_editor import (
    add_group,
    deleted_selected,
    group_names_store,
    layout,
    update,
)


def init_valid_schema(mock=MOCK_SCHEMA):
    Root.schema = mock.copy()
    Root.next_schema = Root.schema


def test_group_names_store():
    assert "Store" in str(group_names_store())


def test_layout():
    init_valid_schema()
    assert isinstance(layout(), html.Div)


def test_deleted_selected_callback() -> None:
    init_valid_schema(mock=MOCK_SCHEMA_WITH_GROUPS_AND_ITEMS)
    selection = [{"name": "group0"}]
    assert deleted_selected(True, selection) == (
        False,
        True,
        ["name0", "name1", "name2"],
    )


def test_add_group():
    init_valid_schema()
    assert add_group(True) == (
        {
            "add": [
                {
                    "name": "<new group name>",
                    "desc": "<add description here>",
                    "order": 0,
                }
            ]
        },
        ["<new group name>"],
    )


def test_update():
    init_valid_schema()
    new_rows = [
        {"name": "Synthesis", "desc": "Synthesis Options", "order": 0},
        {"name": "CTS", "desc": "CTS Options", "order": 1},
        {"name": "DetailRoute", "desc": "Detail Route Options", "order": 2},
        {"name": "Fruit", "desc": "Choose some fruit quantities", "order": 3},
    ]
    assert update(True, new_rows) == (
        False,
        [
            "Synthesis",
            "CTS",
            "DetailRoute",
            "Fruit",
        ],
    )
