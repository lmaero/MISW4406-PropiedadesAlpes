from __future__ import annotations
from dataclasses import dataclass, field
from pda.seedwork.domain.events import (DomainEvent)
from pda.modules.properties.domain.events import (TransactionEvent)
from datetime import datetime
import uuid

class TenantEvent(DomainEvent):
    pass


@dataclass
class CreatedTransaction(TransactionEvent):
    id_transaction: uuid.UUID = None
    id_tenant: uuid.UUID = None
    status: str = None
    created_at: datetime = None
    
@dataclass
class CancelledTransaction(TransactionEvent):
    id_transaction: uuid.UUID = None
    updated_at: datetime = None

@dataclass
class ApprovedTransaction(TransactionEvent):
    id_transaction: uuid.UUID = None
    updated_at: datetime = None

@dataclass
class PaidTransaction(TransactionEvent):
    id_transaction: uuid.UUID = None
    updated_at: datetime = None