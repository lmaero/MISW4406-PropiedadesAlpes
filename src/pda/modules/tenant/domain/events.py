from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from pda.seedwork.domain.events import DomainEvent

@dataclass
class CreatedTenant(DomainEvent):
    id_tenant: uuid.UUID = None
    name: str = None
    email: str = None
    guarantor_name: str = None
    created_at: datetime = None
    updated_at: datetime = None