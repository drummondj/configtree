from src.helpers.validators import (
    validate_alpha_num,
    validate_not_blank,
    validate_version_number,
    validate_type,
)


def test_validate_alpha_num():
    assert validate_alpha_num("a_b_X_Y_123")
    assert not validate_alpha_num("#")


def test_validate_not_blank():
    assert validate_not_blank("a_b_X_Y_123")
    assert not validate_not_blank("")
    assert not validate_not_blank(" ")
    assert not validate_not_blank("  ")
    assert not validate_not_blank("\t")
    assert not validate_not_blank("\n")


def test_validate_version_number():
    assert validate_version_number("0.1.2")
    assert validate_version_number("12.34.56")
    assert not validate_version_number("0.1")
    assert not validate_version_number("0.1.0.1")
    assert not validate_version_number("20240325")


def test_validate_type():
    assert validate_type("", str)
    assert validate_type("I am a string", str)
    assert not validate_type("0.1", str)
    assert not validate_type("100", str)

    assert validate_type("true", bool)
    assert validate_type("false", bool)
    assert validate_type("1", bool)
    assert validate_type("0", bool)
    assert not validate_type("", bool)
    assert not validate_type("I am not a bool", bool)

    assert validate_type("1.0", float)
    assert not validate_type("1", float)
    assert not validate_type("xxx", float)

    assert validate_type("1", int)
    assert not validate_type("1.0", int)
    assert not validate_type("xxx", int)
