import src.model.schema as schema_factory
from src.model.config import Config, ConfigItem
from src.model.schema import Schema


class TestConfig:
    def create_config(self) -> Config:
        return Config("name", "desc", "test/input_schema.json")

    def test_init(self) -> None:
        config = self.create_config()
        assert config.name == "name"
        assert config.desc == "desc"
        assert config.schema_path == "test/input_schema.json"
        assert isinstance(config.schema, Schema)

    def test_generate_items(self) -> None:
        config = self.create_config()
        config.schema = None
        assert config.generate_items() is None

        config = self.create_config()
        config.generate_items()
        assert len(config.items) == 3

    def test_save(self) -> None:
        config: Config = self.create_config()
        config.generate_items()
        config.save("test/config.json")

    def test_validate_desc(self) -> None:
        config: Config = self.create_config()
        config.desc = ""
        config.validate_desc()
        assert len(config.errors) == 1

    def test_validate_name(self) -> None:
        config: Config = self.create_config()
        config.name = ""
        config.validate_name()
        assert len(config.errors) == 1


class TestConfigItem:
    def test_init(self) -> None:
        schema = schema_factory.load("test/input_schema.json")
        schema_item = schema.items[0]
        config_item = ConfigItem(schema_item, "value")
        assert config_item.schema_item == schema_item
        assert config_item.value == "value"
