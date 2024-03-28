"""Contains application state"""

from src.model.config import Config
from src.model.schema import Schema


class Root:
    schema: Schema | None = None
    next_schema: Schema | None = None
    schema_filename: str | None = None

    config: Config | None = None
    next_config: Config | None = None
    config_filename: str | None = None
