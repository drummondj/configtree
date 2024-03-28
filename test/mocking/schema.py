"""Mocking instances for testing"""

from src.model.schema import Schema, SchemaGroup, SchemaItem, SchemaItemType

MOCK_SCHEMA = Schema("name", "desc", "0.0.0")

MOCK_SCHEMA_WITH_GROUPS_AND_ITEMS = Schema(
    "name",
    "desc",
    "0.0.0",
    groups=[
        SchemaGroup("name0", "desc0"),
        SchemaGroup("name1", "desc1"),
        SchemaGroup("name2", "desc2"),
    ],
    items=[
        SchemaItem("name0", "desc0", "name0", "", SchemaItemType.str),
        SchemaItem("name1", "desc1", "name1", "", SchemaItemType.str),
        SchemaItem("name2", "desc2", "name2", "", SchemaItemType.str),
    ],
)
