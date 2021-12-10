"""Defines a basic message structure."""

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Message():
    msg: str
    sender: str
    metadata: dict = field(default_factory=dict)
    id: UUID = field(default_factory=uuid4)
    
