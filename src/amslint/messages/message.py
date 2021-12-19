"""Defines a basic message structure."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Message():
    msg: str
    sender: str
    metadata: dict[Any, Any] = field(default_factory=dict)
