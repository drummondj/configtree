from test.mocking.schema import MOCK_SCHEMA

from src.app_state import Root
from src.components.schema_editor.schema_editor import (
    alerts,
    desc_input,
    layout,
    name_input,
    needs_save,
    save,
    save_button,
    validate_and_set_desc,
    validate_and_set_name,
    validate_and_set_version,
    version_input,
)


def init_valid_schema():
    Root.schema = MOCK_SCHEMA
    Root.next_schema = Root.schema.copy()


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
    init_valid_schema()
    Root.schema_filename = "test/test_schema_editor.json"
    if Root.next_schema is None:
        assert False
    else:
        assert save(True) == (True, True, False, [])

        Root.next_schema.version = "not a version"
        result = save(True)
        assert not result[0]
        assert not result[1]
        assert result[2]
        print(result[3])
        assert len(result[3]) == 3


def test_needs_save():
    init_valid_schema()
    if Root.next_schema is None:
        assert False
    else:
        assert needs_save("_", "_", "_")
        Root.next_schema.name = "new_name___"
        assert not needs_save("_", "_", "_")


def test_alerts():
    assert "Alert" in str(alerts())


def test_layout():
    assert "Form" in str(layout("test/test_schema_editor.json"))
    assert "File missing.json does not exist" in str(layout("missing.json"))
