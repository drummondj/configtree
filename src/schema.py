"""Schema dataclasses for modeling a schema"""

from dataclasses import dataclass, field, replace
from typing import List, Any
from enum import Enum
from dataclass_wizard import JSONWizard
import json


class SchemaValidationException(Exception):
    def __init__(self, error: str, name: str, type: str):
        self.error = error
        self.name = name
        self.type = type
        super().__init__(f"{error} on {name = } {type = }")


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

    def validate_default(self) -> None:
        if self.type == SchemaItemType.int:
            try:
                _ = int(self.default)
            except ValueError:
                raise SchemaValidationException(
                    f"default value {self.default} is not an Integer", self.name, "item"
                )

    def validate(self) -> None:
        self.validate_default()


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

    def save(self, filename) -> None:
        self.validate()
        with open(filename, "w") as f:
            f.write(json.dumps(self.to_dict(), indent=4))

    def validate(self) -> None:
        for item in self.items:
            item.validate()


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
