from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from pda.seedwork.domain.events import DomainEvent


@dataclass
class CreatedTransaction(DomainEvent):
    id_transaction: uuid.UUID = None
    id_client: uuid.UUID = None
    event_date: datetime = None
