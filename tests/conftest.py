import pytest

from amslint.messages import handler

@pytest.fixture
def message_handler():
    return handler.MessageHandler()