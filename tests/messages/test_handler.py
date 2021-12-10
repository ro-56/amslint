"""Tests for the message handler class"""
import pytest


def test_message_handler(message_handler):
    """
    Test the message handler
    """
    assert message_handler is not None


def test_open_channel(message_handler):
    """
    Test opening a channel
    """
    channel = message_handler.open_channel("test_channel", "CUSTOM")
    assert message_handler._channel_exists("test_channel")
    assert channel.type.name == "CUSTOM"


def test_open_channel_with_same_name(message_handler):
    """
    Test opening a channel with the same name
    """
    message_handler.open_channel("test_channel", "CUSTOM")
    with pytest.raises(ValueError):
        message_handler.open_channel("test_channel", "CUSTOM")


def test_close_channel(message_handler):
    """
    Test closing a channel
    """
    message_handler.open_channel("test_channel", "CUSTOM")
    assert message_handler._channel_exists("test_channel")
    message_handler.close_channel(channel_name="test_channel")
    assert message_handler._channel_exists("test_channel")
    assert not message_handler._channel_is_active("test_channel")

def test_flush_closed_channel(message_handler):
    """
    Test flushing closed channels
    """
    message_handler.open_channel("test_channel", "CUSTOM")
    assert message_handler._channel_exists("test_channel")
    message_handler.close_channel(channel_name="test_channel")
    assert message_handler._channel_exists("test_channel")
    assert not message_handler._channel_is_active("test_channel")
    message_handler.flush_closed_channels()
    assert not message_handler._channel_exists("test_channel")


def test_open_channel_without_type(message_handler):
    """
    Test opening a channel without any type
    """
    channel = message_handler.open_channel("test_channel")
    assert message_handler._channel_exists("test_channel")
    assert channel.type.name == "UNKNOWN"


def test_send_message_to_channel(message_handler):
    """
    Test sending a message to a specific channel
    """
    message_handler.open_channel("test_channel", "custom")
    message_handler.send_message(channel_name="test_channel", msg="test_message")
    assert len(message_handler.get_messages(channel_name="test_channel")) == 1


def test_send_message_with_metadata(message_handler):
    """
    Test sending a message with metadata
    """
    message_handler.open_channel("test_channel", "custom")
    metadata = {"test_key": "test_value"}
    message_handler.send_message(channel_name="test_channel", msg="test_message", metadata=metadata)
    assert len(message_handler.get_messages(channel_name="test_channel")) == 1
    assert message_handler.get_messages(channel_name="test_channel")[0].metadata == metadata


def test_send_message_to_default_service_channel(message_handler):
    """
    Test sending a message to the default service channel
    """
    message_handler.send_service_messages(msg="test_message")
    assert len(message_handler.get_service_messages()) == 1


def test_send_message_to_default_channel(message_handler):
    """
    Test sending a message to the default channel
    """
    message_handler.send_message(msg="test_message")
    assert len(message_handler.get_messages_from_default()) == 1


def test_default_service_channel_type(message_handler):
    """
    Test the default service channel type
    """
    assert message_handler.default_service_channel.type.name == "SERVICE"


def test_default_channel_type(message_handler):
    """
    Test the default channel type
    """
    assert message_handler.default_channel.type.name == "CUSTOM"


def test_get_invalid_channel(message_handler):
    """
    Test getting an invalid channel
    """
    with pytest.raises(ValueError):
        assert message_handler._get_channel("test_channel")


def test_get_messages_from_not_existing_channel(message_handler):
    """
    Test getting messages from an invalid channel
    """
    assert not message_handler.get_messages("test_channel")
