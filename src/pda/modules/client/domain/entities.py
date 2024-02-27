from dataclasses import dataclass, field
from datetime import datetime

from pda.seedwork.domain.entities import Entity
from .value_objects import Name, Email, NationalID, Rut


@dataclass
class User(Entity):
    name: Name = field(default_factory=Name)
    email: Email = field(default_factory=Email)


@dataclass
class NaturalClient(User):
    national_id: NationalID = field(default_factory=NationalID)
    birth_date: datetime = field(default_factory=datetime.now)


@dataclass
class EnterpriseClient(User):
    rut: Rut = field(default_factory=Rut)
    creation_date: datetime = field(default_factory=datetime.now)
