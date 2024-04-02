"""Configuration classes"""

import json
import os
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, List

from dataclass_wizard import JSONWizard, json_field

import src.helpers.validators as validators
import src.model.schema as schema_factory
from src.model.schema import Schema, SchemaItem, SchemaValidationError


@dataclass
class ConfigItem(JSONWizard):
    schema_item: SchemaItem
    value: Any = None

    def to_dict(self) -> dict:
        merged_dict = self.schema_item.to_dict().copy()
        merged_dict.update(super().to_dict())
        return merged_dict


@dataclass
class Config(JSONWizard):
    name: str
    desc: str
    schema_path: str
    schema: Schema | None = None
    items: List["ConfigItem"] = field(default_factory=list)
    errors: List["SchemaValidationError"] = json_field(
        "errors", default_factory=list, dump=False
    )  # type: ignore

    def __post_init__(self) -> None:
        if os.path.exists(self.schema_path):
            self.schema = schema_factory.load(self.schema_path)

    def generate_items(self) -> None:
        if self.schema is None:
            return

        self.items = []
        for schema_item in self.schema.items:
            self.items.append(ConfigItem(schema_item, value=schema_item.default))

    def sort_by_group_then_name(self) -> None:
        self.items.sort(
            key=lambda item: (item.schema_item.group, item.schema_item.name)
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

    def validate(self) -> bool:
        self.errors = []
        self.validate_name()
        self.validate_desc()
        # TODO: validate options
        if len(self.errors) == 0:
            return True
        else:
            return False

    def get_errors(self) -> List[SchemaValidationError]:
        all_errors = self.errors.copy()
        # for item in self.items:
        #     all_errors.extend(item.errors)
        return all_errors

    def save(self, filename: str) -> bool:
        if self.validate():
            with open(filename, "w") as f:
                f.write(json.dumps(self.to_dict(), indent=4))
            return True
        else:
            return False

    def copy(self) -> "Config":
        return deepcopy(self)


def from_json(string: str) -> Config:
    configs = Config.from_json(string)
    if isinstance(configs, list):
        # TODO: throw something
        config = configs[0]
    else:
        config = configs

    config.sort_by_group_then_name()
    return config


def load(filename: str) -> Config:
    with open(filename) as f:
        return from_json(f.read())
