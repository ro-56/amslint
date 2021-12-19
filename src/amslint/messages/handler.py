""""""

from typing import Any, Optional

from amslint.messages.channel import MessageChannel
from amslint.messages.message import Message


class MessageHandler():
    """
    A class that represents a message handler.
    """

    active_channels: list[MessageChannel]
    closed_channels: list[MessageChannel]
    default_service_channel: Optional[MessageChannel] = None
    default_channel: Optional[MessageChannel] = None

    def __init__(self) -> None:
        self.active_channels = []
        self.closed_channels = []
        self.initialize()

        return

    def initialize(self) -> None:
        """
        Initialize the message handler.
        """
        if not self.active_channels:
            self.default_service_channel = self.open_channel("Default Service Channel", "service", "Default Service Channel")
            self.default_channel = self.open_channel("Default Channel", "custom", "Default Channel")

        return

    def all_channel(self) -> list[MessageChannel]:
        """
        Get all registered channels.
        """
        all_channels = self.active_channels + self.closed_channels
        return all_channels

    def open_channel(self, channel_name: str, type: str = "", channel_description: str = "") -> MessageChannel:
        """
        Open a channel.
        """
        if self._channel_exists(channel_name):
            raise ValueError(f"Channel {channel_name} already exists.")

        if type:
            new_channel = MessageChannel(name=channel_name, init_type=type, description=channel_description)
        else:
            new_channel = MessageChannel(name=channel_name, description=channel_description)

        self.active_channels.append(new_channel)

        return new_channel

    def close_channel(self, channel_name: str) -> None:
        """
        Close a channel.
        """
        channel = self._get_channel(channel_name)
        if channel:
            self.active_channels.remove(channel)
            self.closed_channels.append(channel)

        return

    def flush_closed_channels(self) -> None:
        """
        Flush closed channels.
        """
        self.closed_channels = []

        return

    def _channel_exists(self, channel_name: str) -> bool:
        """
        Check if a channel exists.
        """
        return channel_name in [channel.name for channel in self.all_channel()]

    def _channel_is_active(self, channel_name: str) -> bool:
        """
        Check if a channel is active.
        """
        return channel_name in [channel.name for channel in self.active_channels]

    def _get_channel(self, channel_name: str) -> MessageChannel:
        """
        Get a channel.
        """
        if not self._channel_exists(channel_name):
            raise ValueError(f"Channel {channel_name} does not exist.")

        channel = [channel for channel in self.all_channel() if channel.name == channel_name][0]

        return channel

    def send_message(self, msg: str, channel_name: Optional[str] = None, metadata: Optional[dict[Any, Any]] = None) -> None:
        if channel_name and self._channel_exists(channel_name):
            channel = self._get_channel(channel_name)
            channel.send_message(msg=msg, metadata=metadata)
        else:
            if self.default_channel:
                self.default_channel.send_message(msg=msg, metadata=metadata)
            else:
                raise ValueError("No default channel is open.")

    def get_messages(self, channel_name: Optional[str] = None) -> list[Message]:
        if channel_name and self._channel_exists(channel_name):
            channel = self._get_channel(channel_name)
            return channel.messages
        else:
            return []

    def get_messages_from_default(self) -> list[Message]:
        if self.default_channel:
            return self.default_channel.messages
        else:
            return []

    def send_service_messages(self, msg: str, metadata: Optional[dict[Any, Any]] = None) -> None:
        if self.default_service_channel:
            self.default_service_channel.send_message(msg=msg, metadata=metadata)
        else:
            raise ValueError("No default service channel is open.")

        return

    def get_service_messages(self) -> list[Message]:
        if self.default_service_channel:
            return self.default_service_channel.messages
        else:
            return []
