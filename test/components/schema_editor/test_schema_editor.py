from typing import Any
import src.components.schema_editor.schema_editor as schema_editor
from src.components.schema_editor.schema_editor import (
    set_if_valid,
    name_input,
    validate_and_set_name,
    validate_and_set_desc,
    validate_and_set_version,
    save_button,
    desc_input,
    version_input,
    save,
    needs_save,
    alerts,
    layout,
)
from src.model.schema import SchemaValidationError


def test_set_if_valid():
    def valid_validator(value: Any):
        return True

    assert set_if_valid("name", "test", valid_validator)

    def invalid_validator(value: Any):
        return False

    assert not set_if_valid("name", "test", invalid_validator)


def test_name_input():
    assert "Input(id='name'" in str(name_input("test"))


def test_validate_and_set_name_callback():
    assert not validate_and_set_name("test")
    assert validate_and_set_name("#invalid#")


def test_desc_input():
    assert "Input(id='desc'" in str(desc_input("test"))


def test_validate_and_set_desc_callback():
    assert not validate_and_set_desc("test##\n")
    assert validate_and_set_desc("")


def test_version_input():
    assert "Input(id='version'" in str(version_input("test"))


def test_validate_and_set_version_callback():
    assert not validate_and_set_version("20.01.22")
    assert not validate_and_set_version("2.1.2")
    assert validate_and_set_version("")
    assert validate_and_set_version("2.1")


def test_save_button():
    repr = str(save_button())
    assert "Button" in repr
    assert "id='save-button'" in repr


def test_save_callback():
    schema_editor.filename = "test/test_schema_editor.json"
    print(schema_editor.next_schema.get_errors())
    assert save(True) == (True, True, False, [])

    schema_editor.next_schema.version = "not a version"
    assert save(True) == (
        False,
        False,
        True,
        [
            "invalid version number not a version on schema row 'test' and column 'version'"
        ],
    )

    assert save(False) == (False, False, False, [])


def test_needs_save():
    schema_editor.schema = schema_editor.next_schema.copy()
    assert needs_save("_", "_", "_")
    schema_editor.next_schema.name = "new_name"
    assert not needs_save("_", "_", "_")


def test_alerts():
    assert "Alert" in str(alerts())


def test_layout():
    assert "Form" in str(layout("test/test_schema_editor.json"))
    assert "File missing.json does not exist" in str(layout("missing.json"))
