import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html

from src.app_state import Root
from src.model.schema import SchemaGroup


# ---------------------------------------------------------------------------------------------------
# Group Names Store (for item_editor)
# ---------------------------------------------------------------------------------------------------
def group_names_store():
    return dcc.Store(id="group-names-store")


# ---------------------------------------------------------------------------------------------------
# Group Editor
# ---------------------------------------------------------------------------------------------------
def layout() -> html.Div:
    if Root.next_schema is None:
        return html.Div("Schema loading, please wait ...")

    columnDefs = [
        {
            "field": "name",
            "headerName": "Group",
            "editable": True,
            "checkboxSelection": True,
            "filter": True,
            "flex": 4,
        },
        {
            "field": "order",
            "headerName": "Order",
            "editable": True,
            "flex": 1,
            "cellDataType": "number",
            "cellEditor": "agNumberCellEditor",
            "cellEditorParams": {
                "min": 0,
                "precision": 0,
                "showStepperButtons": True,
            },
        },
        {
            "field": "desc",
            "headerName": "Description",
            "editable": True,
            "flex": 8,
            "cellEditorPopup": True,
            "cellEditor": "agLargeTextCellEditor",
            "cellRenderer": "markdown",
            "autoHeight": True,
            "cellEditorParams": {
                "maxLength": 16_777_215,
            },
            "wrapText": True,
        },
    ]
    rowData = []
    for group in Root.next_schema.groups:
        rowData.append(group.to_dict())

    grid = dag.AgGrid(
        id="group-data-grid",
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
            group_names_store(),
            html.H2("Groups", className="editor-header"),
            grid,
            html.Div(
                className="toolbar",
                children=[
                    dbc.Button(
                        " Add Group",
                        id="group-add",
                        color="success",
                        className="bi bi-plus-lg mu-3",
                        size="sm",
                    ),
                    dbc.Button(
                        " Delete Group",
                        id="group-del",
                        color="danger",
                        className="bi bi-trash mu-3",
                        size="sm",
                    ),
                ],
            ),
        ]
    )


@callback(
    Output(
        "save-button",
        "disabled",
        allow_duplicate=True,
    ),
    Output("group-data-grid", "deleteSelectedRows"),
    Output("group-names-store", "data", allow_duplicate=True),
    Input("group-del", "n_clicks"),
    State("group-data-grid", "selectedRows"),
    prevent_initial_call=True,
)
def deleted_selected(n_clicks, selection):
    if Root.next_schema is None:
        return True, False, []

    for row in selection:
        for group in Root.next_schema.groups:
            if group.name == row["name"]:
                Root.next_schema.groups.remove(group)
    return False, True, Root.next_schema.get_group_names()


@callback(
    Output("group-data-grid", "rowTransaction"),
    Output("group-names-store", "data", allow_duplicate=True),
    Input("group-add", "n_clicks"),
    prevent_initial_call=True,
)
def add_group(_):
    """Adds an empty group to the top of the table"""
    if Root.next_schema is None:
        return {}, []
    group = SchemaGroup(name="<new group name>", desc="<add description here>")
    Root.next_schema.groups.append(group)
    return {"add": [group.to_dict()]}, Root.next_schema.get_group_names()


@callback(
    Output(
        "save-button",
        "disabled",
        allow_duplicate=True,
    ),
    Output("group-names-store", "data", allow_duplicate=True),
    Input("group-data-grid", "cellValueChanged"),
    State("group-data-grid", "rowData"),
    prevent_initial_call=True,
)
def update(_, rows):
    if Root.next_schema is None:
        return True, []
    Root.next_schema.groups.clear()
    for row in rows:
        Root.next_schema.groups.append(SchemaGroup.from_dict(row))
    return False, Root.next_schema.get_group_names()
