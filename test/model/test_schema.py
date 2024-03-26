import os
import src.model.schema as schema_factory

from src.model.schema import (
    SchemaValidationError,
    SchemaItemType,
    SchemaItem,
    SchemaGroup,
    Schema,
)


class TestSchemaValidationError:
    def test_init(self):
        schema_validation_error = SchemaValidationError(
            "something went wrong", "row", "item", "col"
        )
        assert schema_validation_error.error == "something went wrong"
        assert schema_validation_error.name == "row"
        assert schema_validation_error.type == "item"
        assert schema_validation_error.field == "col"
        assert (
            schema_validation_error.message
            == "something went wrong on item row 'row' and column 'col'"
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
        schema_item = self.create_schema_item()
        schema_item.options = "one two three"
        assert schema_item.validate()
        schema_item.default = "1.0"
        assert not schema_item.validate()


class TestSchemaGroup:
    def test_init(self):
        schema_group = SchemaGroup("name", "desc")
        assert schema_group.name == "name"
        assert schema_group.desc == "desc"
        assert schema_group.order == 0


class TestSchema:
    def create_schema(self):
        return schema_factory.load("test/input_schema.json")

    def test_init(self):
        schema = self.create_schema()
        assert isinstance(schema, Schema)
        assert schema.name == "chip_implementation_schema"
        assert (
            schema.desc
            == "This schema is used to configure all physical implemention stages"
        )
        assert schema.version == "0.1.2"
        assert len(schema.groups) == 4
        assert len(schema.items) == 3

    def test_copy(self):
        schema = self.create_schema()
        schema_copy = schema.copy()
        assert schema is not schema_copy
        assert schema == schema_copy

    def test_eq(self):
        schema = self.create_schema()
        schema_copy = schema.copy()
        assert schema.__eq__(schema_copy)
        schema_copy.name = "new"
        assert not schema.__eq__(schema_copy)
        # TODO: add tests for other field updates in an elegant way

    def test_get_group_names(self):
        schema = self.create_schema()
        assert schema.get_group_names() == [
            "Synthesis",
            "Clock Tree Synthesis",
            "Detail Route",
            "Fruit",
        ]

    def test_update(self):
        schema = self.create_schema()
        assert schema.name == "chip_implementation_schema"
        schema.update("name", "new")
        assert schema.name == "new"

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
        assert len(errors) == 1
        assert not os.path.exists(fn)

        schema.items.append(
            SchemaItem("invalid", "invalid", "group", "default", SchemaItemType.int)
        )
        assert not schema.save(fn)
        assert len(errors) == 2
        assert not os.path.exists(fn)

    def test_get_errors(self):
        schema = self.create_schema()
        assert schema.get_errors() == []
        error = SchemaValidationError("error", "name", "type", "field")
        schema.errors.append(error)
        assert schema.get_errors() == [error]


def test_from_json():
    with open("test/input_schema.json") as f:
        json_data = f.read()

    schema = schema_factory.from_json(json_data)
    assert isinstance(schema, Schema)

    schema = schema_factory.from_json(f"[{json_data},{json_data}]")
    assert isinstance(schema, Schema)


def test_load():
    schema = schema_factory.load("test/input_schema.json")
    assert isinstance(schema, Schema)
