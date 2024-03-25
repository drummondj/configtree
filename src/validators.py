"""A set of validators for forms"""

import re


def validate_alpha_num(text: str) -> bool:
    if re.match("^[a-zA-Z0-9_]+$", text):
        return True
    else:
        return False


def validate_not_blank(text: str) -> bool:
    valid = True
    if text is None:
        valid = False
    elif text.strip() == "":
        valid = False
    return valid


def validate_version_number(text: str) -> bool:
    if re.match("^[0-9]+\\.[0-9]+\\.[0-9]+$", text):
        return True
    else:
        return False