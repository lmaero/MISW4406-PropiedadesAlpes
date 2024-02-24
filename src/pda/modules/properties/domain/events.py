from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from pda.seedwork.domain.events import EventDomain


@dataclass
class CreatedProperty(EventDomain):
    id_property: uuid.UUID = None
    availability: bool = None
    created_at: datetime = None


@dataclass
class LeasedProperty(EventDomain):
    id_tenant: uuid.UUID = None
    updated_at: datetime = None


@dataclass
class ReturnedProperty(EventDomain):
    id_property: uuid.UUID = None
    id_tenant: uuid.UUID = None
    updated_at: datetime = None
