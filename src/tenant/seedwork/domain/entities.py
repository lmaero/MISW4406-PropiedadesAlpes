import uuid
from dataclasses import dataclass, field
from datetime import datetime

from .events import DomainEvent
from .exceptions import ImmutableEntityIdException
from .mixins import ValidateMixinRules
from .rules import ImmutableEntityId


@dataclass
class Entity:
    id: uuid.UUID = field(hash=True)
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())

    @classmethod
    def next_id(cls) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: uuid.UUID) -> None:
        if not ImmutableEntityId(self).is_valid():
            raise ImmutableEntityIdException()
        self._id = self.next_id()


@dataclass
class RootAggregation(Entity, ValidateMixinRules):
    events: list[DomainEvent] = field(default_factory=list)
    compensation_events: list[DomainEvent] = field(default_factory=list)

    def add_event(self, event: DomainEvent, compensation_event: DomainEvent = None):
        self.events.append(event)

        if compensation_event:
            self.compensation_events.append(compensation_event)

    def clean_events(self):
        self.events = list()
        self.compensation_events = list()


@dataclass
class Location(Entity):
    def __str__(self) -> str: ...
