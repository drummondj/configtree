from test.mocking.config import MOCK_CONFIG_WITH_ITEMS

from src.app_state import Root
from src.components.config_editor.item_editor import layout, update


def test_layout() -> None:
    Root.next_config = None
    assert "No config loaded, please wait ..." in str(layout())

    Root.next_config = MOCK_CONFIG_WITH_ITEMS
    assert "Items" in str(layout())


def test_update_callback():
    Root.next_config = None
    assert not update(None, [])

    Root.next_config = MOCK_CONFIG_WITH_ITEMS
    assert not update(None, [{"name": "name0", "value": "new_value"}])
