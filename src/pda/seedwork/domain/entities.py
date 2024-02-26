import uuid
from dataclasses import dataclass, field
from datetime import datetime

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


@dataclass
class RootAggregation(Entity, ValidateMixinRules):
    pass


@dataclass
class Locacion(Entity):
    def __str__(self) -> str:
        pass
