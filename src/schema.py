"""Schema dataclasses for modeling a schema"""

from dataclasses import dataclass, field, replace
from functools import reduce
from typing import List, Any
from enum import Enum
from dataclass_wizard import JSONWizard
import json
import src.helpers.validators as validators


@dataclass
class SchemaValidationError:
    def __init__(self, error: str, name: str, type: str, field: str):
        self.error = error
        self.name = name
        self.type = type
        self.message = f"{error} on {type} row '{name}' and column '{field}'"


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
    errors: List[SchemaValidationError] = field(default_factory=list)

    def __validate_field_type__(self, field: str, value: str) -> None:
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
                    f"Value '{value}' is not a '{type_error}'",
                    self.name,
                    "item",
                    field,
                )
            )

    def validate_default(self) -> None:
        self.__validate_field_type__("default", self.default)

    def validate_options(self) -> None:
        for value in self.options.split():
            self.__validate_field_type__("options", value)

    def validate(self) -> bool:
        self.errors = []
        self.validate_default()
        self.validate_options()
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


@dataclass
class Schema(JSONWizard):
    """A schema is the top level schema dataclass that holds all schema groups"""

    name: str
    desc: str
    version: str
    groups: List["SchemaGroup"] = field(default_factory=list)
    items: List["SchemaItem"] = field(default_factory=list)

    def copy(self) -> "Schema":
        return replace(self)

    def __eq__(self, other) -> bool:
        # TODO: add groups and items comparison
        return (
            self.name == other.name
            and self.desc == other.desc
            and self.version == other.version
        )

    def get_group_names(self) -> List[str]:
        return [group.name for group in self.groups]

    def update(self, name: str, value: Any):
        setattr(self, name, value)

    def save(self, filename) -> bool:
        if self.validate():
            with open(filename, "w") as f:
                f.write(json.dumps(self.to_dict(), indent=4))
            return True
        else:
            return False

    def validate(self) -> bool:
        passed = True
        for item in self.items:
            if not item.validate():
                passed = False
        return passed

    def errors(self) -> List[SchemaValidationError]:
        errors = []
        for item in self.items:
            errors.extend(item.errors)
        return errors


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
