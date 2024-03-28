from typing import Literal

import dash_ag_grid as dag
from dash import Input, Output, State, callback, html

from src.app_state import Root


def layout() -> html.Div:
    if Root.next_config is None:
        return html.Div("No config loaded, please wait ...")

    columnDefs = [
        {"field": "group", "headerName": "Group", "flex": 4, "filter": True},
        {
            "field": "name",
            "headerName": "Item",
            "filter": True,
            "flex": 4,
        },
        {
            "field": "value",
            "headerName": "Value",
            "filter": True,
            "editable": True,
            "flex": 4,
            "cellEditor": {"function": "CustomConfigValueEditor"},
        },
        {
            "field": "desc",
            "headerName": "Description",
            "flex": 8,
            "cellRenderer": "markdown",
            "autoHeight": True,
        },
        {
            "field": "default",
            "headerName": "Default Value",
            "flex": 2,
            "hide": True,
        },
        {
            "field": "type",
            "headerName": "Type",
            "flex": 1,
            "hide": True,
        },
        {
            "field": "options",
            "headerName": "Options",
            "flex": 3,
            "hide": True,
        },
    ]
    rowData = []
    for item in Root.next_config.items:
        rowData.append(item.to_dict())

    grid = dag.AgGrid(
        id="config-item-data-grid",
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
        ]
    )


@callback(
    Output(
        "config-save-button",
        "disabled",
        allow_duplicate=True,
    ),
    Input("config-item-data-grid", "cellValueChanged"),
    State("config-item-data-grid", "rowData"),
    prevent_initial_call=True,
)
def update(_, rows) -> Literal[False]:
    if Root.next_config is None:
        return False
    for row in rows:
        for item in Root.next_config.items:
            if item.schema_item.name == row["name"] and item.value != row["value"]:
                item.value = row["value"]
    return False
