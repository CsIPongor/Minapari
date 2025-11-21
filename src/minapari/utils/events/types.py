from typing import Protocol, runtime_checkable

from minapari.utils.events.event import EmitterGroup


@runtime_checkable
class SupportsEvents(Protocol):
    events: EmitterGroup
