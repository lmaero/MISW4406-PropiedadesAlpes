import uuid
from dataclasses import dataclass, field
from datetime import datetime

from .events import EventDomain
from .exceptions import ImmutableIdException
from .mixins import ValidateMixinRules
from .rules import EntityIdImmutable


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
    def id(self, identifier: uuid.UUID) -> None:
        if not EntityIdImmutable(self).is_valid():
            raise ImmutableIdException()
        self._id = self.next_id()


@dataclass
class RootAggregation(Entity, ValidateMixinRules):
    events: list[EventDomain] = field(default_factory=list)

    def add_event(self, event: EventDomain):
        self.events.append(event)

    def clean_events(self):
        self.events = list()


@dataclass
class Transaction(Entity):
    def __str__(self) -> str:
        pass
