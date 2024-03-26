from src.components.schema_editor.group_editor import (
    layout,
    group_names_store,
    deleted_selected,
    add_group,
    update,
)
import src.model.schema as schema
from dash import html
import src.components.schema_editor.schema_editor as schema_editor


def test_group_names_store():
    assert "Store" in str(group_names_store())


def test_layout():
    schema_editor.next_schema = schema.load("test/input_schema.json")
    assert isinstance(layout(schema_editor.next_schema), html.Div)


def test_deleted_selected_callback():
    selection = [{"name": "Synthesis"}]
    assert deleted_selected(True, selection) == (
        False,
        True,
        ["Clock Tree Synthesis", "Detail Route", "Fruit"],
    )


def test_add_group():
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
        ["Clock Tree Synthesis", "Detail Route", "Fruit", "<new group name>"],
    )


def test_update():
    new_rows = [
        {"name": "Synthesis", "desc": "Synthesis Options", "order": 0},
        {"name": "CTS", "desc": "CTS Options", "order": 1},
        {"name": "Detail Route", "desc": "Detail Route Options", "order": 2},
        {"name": "Fruit", "desc": "Choose some fruit quantities", "order": 3},
    ]
    assert update(True, new_rows) == (
        False,
        [
            "Synthesis",
            "CTS",
            "Detail Route",
            "Fruit",
        ],
    )
