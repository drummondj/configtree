"""Schema dataclasses for modeling a schema"""

import json
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List

from dataclass_wizard import JSONWizard, json_field

import src.helpers.validators as validators


@dataclass
class SchemaValidationError:
    def __init__(self, message: str, table: str, row: str, col: str):
        self.message = message
        self.table = table
        self.row = row
        self.col = col

    def __repr__(self):
        return f"{self.message} ({self.table = } {self.row = } {self.col = })"


class SchemaItemType(Enum):
    """A schema item can be str, bool, int or float"""

    str = "String"
    bool = "Boolean"
    int = "Integer"
    float = "Float"


@dataclass
class SchemaItem(JSONWizard):
    """A schema item represents one variable we want to configure"""

    name: str
    desc: str
    group: str
    default: Any
    type: SchemaItemType
    options: str = ""
    errors: List["SchemaValidationError"] = json_field(
        "errors", default_factory=list, dump=False
    )  # type: ignore

    def __validate_field_type__(self, col: str, value: str) -> None:
        type_error = None
        if self.type == SchemaItemType.int:
            if not validators.validate_type(value, int):
                type_error = "Integer"
        elif self.type == SchemaItemType.bool:
            if not validators.validate_type(value, bool):
                type_error = "Boolean"
        elif self.type == SchemaItemType.float:
            if not validators.validate_type(value, float):
                type_error = "Float"
        elif self.type == SchemaItemType.str:
            if not validators.validate_type(value, str):
                type_error = "String"

        if type_error:
            self.errors.append(
                SchemaValidationError(
                    f"Item {self.name} column '{col}': value '{value}' is not a {type_error}",
                    "item",
                    self.name,
                    col,
                )
            )

    def validate_name(self) -> None:
        if not validators.validate_alpha_num(self.name):
            self.errors.append(
                SchemaValidationError(
                    f"Item {self.name} invalid, must not be blank and only contain a-z, A-Z, 0-9 and _",
                    "item",
                    self.name,
                    "name",
                )
            )

    def validate_desc(self) -> None:
        if not validators.validate_not_blank(self.desc):
            self.errors.append(
                SchemaValidationError(
                    f"Item {self.name} invalid description, must not be blank",
                    "item",
                    self.name,
                    "desc",
                )
            )

    def validate_default(self) -> None:
        self.__validate_field_type__("default", self.default)

    def validate_options(self) -> None:
        for value in self.options.split():
            self.__validate_field_type__("options", value)

    def validate_group(self, parent: "Schema") -> None:
        match = next(
            (group for group in parent.groups if group.name == self.group), None
        )

        if match is None:
            self.errors.append(
                SchemaValidationError(
                    f"Item {self.name} invalid group {self.group}, must be an existing group {parent.get_group_names()}",
                    "item",
                    self.name,
                    "group",
                )
            )

    def validate(self, parent: "Schema") -> bool:
        self.errors = []
        self.validate_name()
        self.validate_desc()
        self.validate_default()
        self.validate_options()
        self.validate_group(parent)
        if len(self.errors) == 0:
            return True
        else:
            return False


@dataclass
class SchemaGroup(JSONWizard):
    """A schema group helps group similar items to make editing large configs easier"""

    name: str
    desc: str
    order: int = 0
    errors: List["SchemaValidationError"] = json_field(
        "errors", default_factory=list, dump=False
    )  # type: ignore

    def validate_name(self) -> None:
        if not validators.validate_alpha_num(self.name):
            self.errors.append(
                SchemaValidationError(
                    f"Group {self.name} invalid, must not be blank and only contain a-z, A-Z, 0-9 and _",
                    "group",
                    self.name,
                    "name",
                )
            )

    def validate_desc(self) -> None:
        if not validators.validate_not_blank(self.desc):
            self.errors.append(
                SchemaValidationError(
                    f"Group {self.name} invalid description, must not be blank",
                    "group",
                    self.name,
                    "desc",
                )
            )

    def validate_order(self) -> None:
        if not validators.validate_type(self.order, int):
            self.errors.append(
                SchemaValidationError(
                    f"Group {self.name} invalid order, must be an Integer",
                    "group",
                    self.name,
                    "order",
                )
            )

    def validate(self) -> bool:
        self.errors = []
        self.validate_name()
        self.validate_desc()
        self.validate_order()
        if len(self.errors) == 0:
            return True
        else:
            return False


@dataclass
class Schema(JSONWizard):
    """A schema is the top level schema dataclass that holds all schema groups"""

    name: str
    desc: str
    version: str
    groups: List["SchemaGroup"] = field(default_factory=list)
    items: List["SchemaItem"] = field(default_factory=list)
    errors: List["SchemaValidationError"] = json_field(
        "errors", default_factory=list, dump=False
    )  # type: ignore

    def copy(self) -> "Schema":
        return deepcopy(self)

    def get_group_names(self) -> List[str]:
        return [group.name for group in self.groups]

    def save(self, filename) -> bool:
        if self.validate():
            with open(filename, "w") as f:
                f.write(json.dumps(self.to_dict(), indent=4))
            return True
        else:
            return False

    def validate_version(self) -> bool:
        if not validators.validate_version_number(self.version):
            self.errors.append(
                SchemaValidationError(
                    f"Schema version number '{self.version}' must be formated as x.y.z",
                    "schema",
                    self.name,
                    "version",
                )
            )
            return False
        return True

    def validate_name(self) -> bool:
        if not validators.validate_alpha_num(self.name):
            self.errors.append(
                SchemaValidationError(
                    f"Schema name {self.name} invalid, must not be blank and only contain a-z, A-Z, 0-9 and _",
                    "schema",
                    self.name,
                    "name",
                )
            )
            return False
        return True

    def validate_desc(self) -> bool:
        if not validators.validate_not_blank(self.desc):
            self.errors.append(
                SchemaValidationError(
                    f"Schema {self.name} invalid description, must not be blank",
                    self.name,
                    "schema",
                    "desc",
                )
            )
            return False
        return True

    def validate(self) -> bool:
        self.errors = []
        self.validate_name()
        self.validate_desc()
        self.validate_version()
        for item in self.items:
            item.validate(self)

        for group in self.groups:
            group.validate()

        return len(self.errors) == 0

    def get_errors(self) -> List[SchemaValidationError]:
        all_errors = self.errors.copy()
        for item in self.items:
            all_errors.extend(item.errors)
        for group in self.groups:
            all_errors.extend(group.errors)
        return all_errors


def from_json(string: str) -> Schema:
    schemas = Schema.from_json(string)
    if isinstance(schemas, list):
        # TODO: throw something
        return schemas[0]
    else:
        return schemas


def load(filename: str) -> Schema:
    with open(filename) as f:
        return from_json(f.read())
