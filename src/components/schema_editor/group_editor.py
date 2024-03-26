from dash import html, dcc, callback, Input, Output, State
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from src.model.schema import Schema, SchemaGroup


# ---------------------------------------------------------------------------------------------------
# Group Names Store (for item_editor)
# ---------------------------------------------------------------------------------------------------
def group_names_store():
    return dcc.Store(id="group-names-store")


# ---------------------------------------------------------------------------------------------------
# Group Editor
# ---------------------------------------------------------------------------------------------------
def layout(schema: Schema) -> html.Div:
    global next_schema
    next_schema = schema
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
        },
    ]
    rowData = []
    for group in next_schema.groups:
        rowData.append(group.to_dict())

    grid = dag.AgGrid(
        id="group-data-grid",
        rowData=rowData,
        columnDefs=columnDefs,
        dashGridOptions={
            "undoRedoCellEditing": True,
            "undoRedoCellEditingLimit": 20,
            "domLayout": "autoHeight",
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
    for row in selection:
        for group in next_schema.groups:
            if group.name == row["name"]:
                next_schema.groups.remove(group)
    return False, True, next_schema.get_group_names()


@callback(
    Output("group-data-grid", "rowTransaction"),
    Output("group-names-store", "data", allow_duplicate=True),
    Input("group-add", "n_clicks"),
    prevent_initial_call=True,
)
def add_group(_):
    """Adds an empty group to the top of the table"""
    group = SchemaGroup(name="<new group name>", desc="<add description here>")
    next_schema.groups.append(group)
    return {"add": [group.to_dict()]}, next_schema.get_group_names()


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
    next_schema.groups.clear()
    for row in rows:
        next_schema.groups.append(SchemaGroup.from_dict(row))
    return False, next_schema.get_group_names()
