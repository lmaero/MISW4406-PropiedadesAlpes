import uuid
from dataclasses import dataclass, field
from datetime import datetime

from .exceptions import ImmutableEntityIdException
from .rules import ImmutableEntityId


@dataclass
class DomainEvent:
    id: uuid.UUID = field(hash=True)
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    event_date: datetime = field(default=datetime.now())

    @classmethod
    def next_id(self) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: uuid.UUID) -> None:
        if not ImmutableEntityId(self).is_valid():
            raise ImmutableEntityIdException()
        self._id = self.next_id()
