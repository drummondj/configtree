import json

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, html

from src.app_state import Root
from src.model.schema import Schema, SchemaItem, SchemaItemType


def layout(schema: Schema) -> html.Div:
    Root.next_schema = schema
    columnDefs = [
        {
            "field": "name",
            "headerName": "Item",
            "editable": True,
            "checkboxSelection": True,
            "filter": True,
            "flex": 4,
        },
        {
            "field": "group",
            "headerName": "Group",
            "editable": True,
            "flex": 2,
            "cellEditor": "agSelectCellEditor",
            "cellEditorParams": {"function": "getGroupNames(params)"},
        },
        {
            "field": "default",
            "headerName": "Default Value",
            "editable": True,
            "flex": 2,
        },
        {
            "field": "type",
            "headerName": "Type",
            "editable": True,
            "flex": 1,
            "cellEditor": "agSelectCellEditor",
            "cellEditorParams": {"values": ["String", "Boolean", "Integer", "Float"]},
        },
        {
            "field": "options",
            "headerName": "Options",
            "editable": True,
            "flex": 3,
        },
        {
            "field": "desc",
            "headerName": "Description",
            "cellRenderer": "markdown",
            "autoHeight": True,
            "editable": True,
            "cellEditorPopup": True,
            "cellEditor": "agLargeTextCellEditor",
            "cellEditorParams": {
                "maxLength": 16_777_215,
            },
            "wrapText": True,
            "flex": 8,
        },
    ]
    rowData = []
    for group in Root.next_schema.items:
        rowData.append(group.to_dict())

    grid = dag.AgGrid(
        id="item-data-grid",
        rowData=rowData,
        columnDefs=columnDefs,
        dashGridOptions={
            "undoRedoCellEditing": True,
            "undoRedoCellEditingLimit": 20,
            "domLayout": "autoHeight",
            "singleClickEdit": True,
            "animateRows": False,
            "stopEditingWhenCellsLoseFocus": True,
        },
        className="ag-theme-alpine compact",
        style={"height": None},
    )
    return html.Div(
        [
            html.H2("Items", className="editor-header"),
            grid,
            html.Div(
                className="toolbar",
                children=[
                    dbc.Button(
                        " Add Item",
                        id="item-add",
                        color="success",
                        className="bi bi-plus-lg",
                        size="sm",
                    ),
                    dbc.Button(
                        " Delete Item",
                        id="item-del",
                        color="danger",
                        className="bi bi-trash",
                        size="sm",
                    ),
                ],
            ),
            html.Div(
                id="group-names-options",
                children=json.dumps(Root.next_schema.get_group_names()),
                hidden=True,
            ),
        ]
    )


@callback(
    Output(
        "save-button",
        "disabled",
        allow_duplicate=True,
    ),
    Output("item-data-grid", "deleteSelectedRows"),
    Input("item-del", "n_clicks"),
    State("item-data-grid", "selectedRows"),
    prevent_initial_call=True,
)
def deleted_selected(n_clicks, selection):
    if Root.next_schema is not None:
        for row in selection:
            for item in Root.next_schema.items:
                if item.name == row["name"]:
                    Root.next_schema.items.remove(item)
    return False, True


@callback(
    Output("item-data-grid", "rowTransaction"),
    Input("item-add", "n_clicks"),
    prevent_initial_call=True,
)
def add_item(_):
    """Adds an empty item to the top of the table"""
    if Root.next_schema is not None:
        item = SchemaItem(
            name="<new item name>",
            desc="<add description here>",
            group="",
            default=None,
            type=SchemaItemType.str,
        )
        Root.next_schema.items.append(item)
        return {
            "add": [item.to_dict()],
        }
    else:
        return {}


@callback(
    Output(
        "save-button",
        "disabled",
        allow_duplicate=True,
    ),
    Input("item-data-grid", "cellValueChanged"),
    State("item-data-grid", "rowData"),
    prevent_initial_call=True,
)
def update(_, rows):
    if Root.next_schema is not None:
        Root.next_schema.items.clear()
        for row in rows:
            Root.next_schema.items.append(SchemaItem.from_dict(row))
    return False


@callback(
    Output("group-names-options", "children"),
    Input("group-names-store", "data"),
    prevent_initial_call=True,
)
def group_name_changed(data):
    return json.dumps(data)
