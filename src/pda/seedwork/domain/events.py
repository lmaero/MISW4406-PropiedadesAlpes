import uuid
from dataclasses import dataclass, field
from datetime import datetime

from .exceptions import ImmutableIdException
from .rules import EntityIdImmutable


@dataclass
class EventDomain:
    id: uuid.UUID = field(hash=True)
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    event_date: datetime = field(default=datetime.now())

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
