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

    def add_event(self, event: DomainEvent):
        self.events.append(event)

    def clean_events(self):
        self.events = list()
