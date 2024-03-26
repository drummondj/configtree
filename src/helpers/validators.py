"""A set of validators for forms and models"""

import re
from typing import Any


def validate_alpha_num(text: str) -> bool:
    if re.match("^[a-zA-Z0-9_]+$", text):
        return True
    else:
        return False


def validate_not_blank(text: str) -> bool:
    return not text.strip() == ""


def validate_version_number(text: str) -> bool:
    if re.match("^[0-9]+\\.[0-9]+\\.[0-9]+$", text):
        return True
    else:
        return False


def validate_type(value: Any, type: type) -> bool:
    # Check built-in conversion first
    try:
        _ = type(value)
    except ValueError:
        return False

    # String should not look like an int or float
    if type is str:
        try:
            _ = int(value)
            return False
        except ValueError:
            try:
                _ = float(value)
                return False
            except ValueError:
                pass

    # Boolean should be true, false, 1 or 0
    if type is bool:
        if value not in ["true", "false", "1", "0"]:
            return False

    # Float should not look like an int
    if type is float:
        try:
            _ = int(value)
            return False
        except ValueError:
            pass

    return True
