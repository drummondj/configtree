from src.validators import (
    validate_alpha_num,
    validate_not_blank,
    validate_version_number,
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
