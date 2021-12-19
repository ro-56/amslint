""""""

from amslint.messages.message import Message
from dataclasses import dataclass, field, InitVar
from enum import Enum, auto
from inspect import getframeinfo, stack
from typing import Any, Optional


@dataclass
class MessageChannel():
    """
    A class that represents a message channel.
    """

    init_type: InitVar[str] = None
    name: str = ""
    description: str = ""
    type: Optional['MessageChannelType'] = None
    messages: list[Message] = field(default_factory=list)

    def __post_init__(self, init_type: str):
        if (not init_type or init_type.upper() not in self.MessageChannelType.__members__):
            self.type = self.MessageChannelType.UNKNOWN
        else:
            self.type = self.MessageChannelType[init_type.upper()]

    def send_message(self, msg: str, metadata: Optional[dict[Any, Any]] = None) -> None:
        """
        Send a message to the channel.
        """
        caller = getframeinfo(stack()[1][0])
        sender = f"{caller.filename}:{caller.lineno}"

        if not metadata:
            messag_obj = Message(msg=msg, sender=sender)
        else:
            messag_obj = Message(msg=msg, sender=sender, metadata=metadata)

        self.messages.append(messag_obj)

        return

    class MessageChannelType(Enum):
        """
        An enum that represents the type of a message channel.
        """
        REPORT = auto()
        SERVICE = auto()
        CUSTOM = auto()
        UNKNOWN = auto()
