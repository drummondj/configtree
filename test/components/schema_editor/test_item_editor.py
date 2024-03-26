from src.components.schema_editor.item_editor import (
    layout,
    deleted_selected,
    add_item,
    update,
    group_name_changed,
)
import src.schema as schema
from dash import html
import src.components.schema_editor.schema_editor as schema_editor


def test_layout():
    schema_editor.next_schema = schema.load("test/input_schema.json")
    assert isinstance(layout(schema_editor.next_schema), html.Div)


def test_deleted_selected_callback():
    selection = [{"name": "synthesis_effort"}]
    assert deleted_selected(True, selection) == (False, True)


def test_add_item():
    assert add_item(True) == {
        "add": [
            {
                "name": "<new item name>",
                "desc": "<add description here>",
                "default": None,
                "group": "",
                "type": "String",
                "options": "",
                "errors": [],
            }
        ]
    }


def test_update():
    new_rows = [
        {
            "name": "item_1",
            "desc": "item_1",
            "group": "",
            "default": "",
            "type": "String",
        },
        {
            "name": "item_2",
            "desc": "item_2",
            "group": "",
            "default": "",
            "type": "String",
        },
        {
            "name": "item_3",
            "desc": "item_3",
            "group": "",
            "default": "",
            "type": "String",
        },
    ]
    assert not update(True, new_rows)


def test_group_name_changed():
    assert group_name_changed({"a": "b", "c": "d"}) == '{"a": "b", "c": "d"}'
