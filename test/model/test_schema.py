import os
from test.mocking.schema import MOCK_SCHEMA_WITH_GROUPS_AND_ITEMS

import src.model.schema as schema_factory
from src.model.schema import (
    Schema,
    SchemaGroup,
    SchemaItem,
    SchemaItemType,
    SchemaValidationError,
)


class TestSchemaValidationError:
    def test_init(self):
        schema_validation_error = SchemaValidationError(
            "something went wrong", "item", "row", "col"
        )
        assert schema_validation_error.message == "something went wrong"
        assert schema_validation_error.table == "item"
        assert schema_validation_error.row == "row"
        assert schema_validation_error.col == "col"
        assert (
            str(schema_validation_error)
            == "something went wrong (self.table = 'item' self.row = 'row' self.col = 'col')"
        )


class TestSchemaItemType:
    def test_init(self):
        assert SchemaItemType.str.value == "String"
        assert SchemaItemType.bool.value == "Boolean"
        assert SchemaItemType.int.value == "Integer"
        assert SchemaItemType.float.value == "Float"


class TestSchemaItem:
    def create_schema_item(self):
        return SchemaItem("name", "desc", "group", "default", SchemaItemType.str)

    def test_init(self):
        schema_item = self.create_schema_item()
        assert schema_item.name == "name"
        assert schema_item.desc == "desc"
        assert schema_item.group == "group"
        assert schema_item.default == "default"
        assert schema_item.options == ""
        assert schema_item.errors == []

    def test_validate_field_type(self):
        schema_item = self.create_schema_item()

        schema_item.errors = []
        schema_item.type = SchemaItemType.str
        schema_item.__validate_field_type__("default", "value")
        assert len(schema_item.errors) == 0
        schema_item.__validate_field_type__("default", "0")
        assert len(schema_item.errors) == 1

        schema_item.errors = []
        schema_item.type = SchemaItemType.int
        schema_item.__validate_field_type__("default", "0")
        assert len(schema_item.errors) == 0
        schema_item.__validate_field_type__("default", "not an int")
        assert len(schema_item.errors) == 1

        schema_item.errors = []
        schema_item.type = SchemaItemType.bool
        schema_item.__validate_field_type__("default", "0")
        assert len(schema_item.errors) == 0
        schema_item.__validate_field_type__("default", "not a bool")
        assert len(schema_item.errors) == 1

        schema_item.errors = []
        schema_item.type = SchemaItemType.float
        schema_item.__validate_field_type__("default", "0.0")
        assert len(schema_item.errors) == 0
        schema_item.__validate_field_type__("default", "not a float")
        assert len(schema_item.errors) == 1

    def test_validate_name(self):
        schema_item = self.create_schema_item()
        schema_item.validate_name()
        assert len(schema_item.errors) == 0
        schema_item.name = ""
        schema_item.validate_name()
        assert len(schema_item.errors) == 1

    def test_validate_desc(self):
        schema_item = self.create_schema_item()
        schema_item.validate_desc()
        assert len(schema_item.errors) == 0
        schema_item.desc = ""
        schema_item.validate_desc()
        assert len(schema_item.errors) == 1

    def test_validate_default(self):
        schema_item = self.create_schema_item()
        schema_item.validate_default()
        assert len(schema_item.errors) == 0

    def test_validate_options(self):
        schema_item = self.create_schema_item()
        schema_item.options = "one two three"
        schema_item.validate_options()
        assert len(schema_item.errors) == 0

    def test_validate(self):
        parent = Schema("name", "desc", "0.1.0")
        parent.groups.append(SchemaGroup("group", "test group"))
        schema_item = self.create_schema_item()
        schema_item.options = "one two three"
        assert schema_item.validate(parent)
        schema_item.default = "1.0"
        assert not schema_item.validate(parent)


class TestSchemaGroup:
    def create_schema_group(self):
        return SchemaGroup("name", "desc")

    def test_init(self):
        schema_group = self.create_schema_group()
        assert schema_group.name == "name"
        assert schema_group.desc == "desc"
        assert schema_group.order == 0

    def test_validate_name(self):
        schema_group = self.create_schema_group()
        schema_group.validate_name()
        assert len(schema_group.errors) == 0
        schema_group.name = ""
        schema_group.validate_name()
        assert len(schema_group.errors) == 1

    def test_validate_desc(self):
        schema_group = self.create_schema_group()
        schema_group.validate_desc()
        assert len(schema_group.errors) == 0
        schema_group.desc = ""
        schema_group.validate_desc()
        assert len(schema_group.errors) == 1

    def test_validate_order(self):
        schema_group = self.create_schema_group()
        schema_group.validate_order()
        assert len(schema_group.errors) == 0
        schema_group.order = ""  # type: ignore
        schema_group.validate_order()
        assert len(schema_group.errors) == 1

    def test_validate(self):
        schema_group = self.create_schema_group()
        schema_group.validate()
        assert len(schema_group.errors) == 0
        schema_group.name = ""
        schema_group.validate()
        assert len(schema_group.errors) == 1


class TestSchema:
    def create_schema(self):
        return MOCK_SCHEMA_WITH_GROUPS_AND_ITEMS.copy()

    def test_init(self):
        schema = self.create_schema()
        assert isinstance(schema, Schema)
        assert schema.name == "name"
        assert schema.desc == "desc"
        assert schema.version == "0.0.0"
        assert len(schema.groups) == 3
        assert len(schema.items) == 3

    def test_copy(self):
        schema = self.create_schema()
        schema_copy = schema.copy()
        assert schema is not schema_copy
        assert schema == schema_copy

    def test_get_group_names(self):
        schema = self.create_schema()
        assert schema.get_group_names() == [
            "name0",
            "name1",
            "name2",
        ]

    def test_save(self):
        schema = self.create_schema()
        fn = "test/delete_me.json"
        result = schema.save(fn)
        errors = schema.get_errors()
        for error in errors:
            print(error.message)
        assert len(errors) == 0
        assert result
        os.remove(fn)

        schema.version = "invalid_version"
        assert not schema.save(fn)
        assert len(schema.get_errors()) == 1
        assert not os.path.exists(fn)

        schema.items.append(
            SchemaItem("invalid", "invalid", "group", "default", SchemaItemType.int)
        )
        assert not schema.save(fn)
        assert len(schema.get_errors()) == 3
        assert not os.path.exists(fn)

        schema.groups.append(SchemaGroup("", "invalid"))
        assert not schema.save(fn)
        assert len(schema.get_errors()) == 4
        assert not os.path.exists(fn)

    def test_get_errors(self):
        schema = self.create_schema()
        assert schema.get_errors() == []
        error = SchemaValidationError("error", "name", "type", "field")
        schema.errors.append(error)
        assert schema.get_errors() == [error]

    def test_validate_name(self):
        schema = self.create_schema()
        schema.validate_name()
        assert len(schema.errors) == 0
        schema.name = ""
        schema.validate_name()
        assert len(schema.errors) == 1

    def test_validate_desc(self):
        schema = self.create_schema()
        schema.validate_desc()
        assert len(schema.get_errors()) == 0
        schema.desc = ""
        schema.validate_desc()
        assert len(schema.get_errors()) == 1


def test_from_json():
    json_data = MOCK_SCHEMA_WITH_GROUPS_AND_ITEMS.to_json()
    schema = schema_factory.from_json(json_data)
    assert isinstance(schema, Schema)

    schema = schema_factory.from_json(f"[{json_data},{json_data}]")
    assert isinstance(schema, Schema)


def test_load():
    assert MOCK_SCHEMA_WITH_GROUPS_AND_ITEMS.save("test/input_schema.json")
    schema = schema_factory.load("test/input_schema.json")
    assert isinstance(schema, Schema)
