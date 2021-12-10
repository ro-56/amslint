import pytest

from amslint.messages import handler

@pytest.fixture
def message_handler() -> handler.MessageHandler:
    return handler.MessageHandler()