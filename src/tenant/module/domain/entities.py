from dataclasses import dataclass, field
from datetime import datetime

from tenant.seedwork.domain.entities import Entity, RootAggregation
from .value_object import FullName, Email, IdCard, Rut


@dataclass
class Tenant(Entity):
    full_name: FullName = field(default_factory=FullName)
    email: Email = field(default_factory=Email)


@dataclass
class NaturalTenant(Tenant, RootAggregation):
    id_card: IdCard = None
    birthdate: datetime = None


@dataclass
class BussinesTenant(Tenant, RootAggregation):
    rut: Rut = None
    constitution_date: datetime = None
