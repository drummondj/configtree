"""Mocking instances for testing"""

from src.model.config import Config, ConfigItem

from .schema import MOCK_SCHEMA_WITH_GROUPS_AND_ITEMS

MOCK_CONFIG = Config("name", "desc", "schema_path")

MOCK_CONFIG_WITH_ITEMS = Config(
    "name", "desc", "schema_path", schema=MOCK_SCHEMA_WITH_GROUPS_AND_ITEMS
)

MOCK_CONFIG_WITH_ITEMS.generate_items()
