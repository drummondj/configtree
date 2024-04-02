from test.mocking.schema import MOCK_SCHEMA_WITH_GROUPS_AND_ITEMS

from dash import html

from src.app_state import Root
from src.components.schema_editor.item_editor import (
    add_item,
    deleted_selected,
    group_name_changed,
    layout,
    update,
)


def test_layout():
    Root.next_schema = MOCK_SCHEMA_WITH_GROUPS_AND_ITEMS.copy()
    assert isinstance(layout(Root.next_schema), html.Div)


def test_deleted_selected_callback():
    Root.next_schema = MOCK_SCHEMA_WITH_GROUPS_AND_ITEMS.copy()
    selection = [{"name": "name0"}]
    assert deleted_selected(True, selection) == (False, True)


def test_add_item():
    Root.next_schema = None
    assert add_item(True) == {}

    Root.next_schema = MOCK_SCHEMA_WITH_GROUPS_AND_ITEMS.copy()
    assert add_item(True) == {
        "add": [
            {
                "name": "<new item name>",
                "desc": "<add description here>",
                "default": None,
                "group": "",
                "type": "String",
                "options": "",
            }
        ]
    }


def test_update():
    Root.next_schema = MOCK_SCHEMA_WITH_GROUPS_AND_ITEMS.copy()
    new_rows = [
        {
            "name": "item_1",
            "desc": "item_1",
            "group": "syn",
            "default": "",
            "type": "String",
        },
        {
            "name": "item_2",
            "desc": "item_2",
            "group": "syn",
            "default": "",
            "type": "String",
        },
        {
            "name": "item_3",
            "desc": "item_3",
            "group": "syn",
            "default": "",
            "type": "String",
        },
    ]
    assert not update(True, new_rows)


def test_group_name_changed():
    assert group_name_changed({"a": "b", "c": "d"}) == '{"a": "b", "c": "d"}'
