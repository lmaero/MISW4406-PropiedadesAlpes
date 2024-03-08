from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from pda.seedwork.domain.events import DomainEvent


class TransactionEvent(DomainEvent):
    pass


@dataclass
class CreatedTransaction(TransactionEvent):
    id_transaction: uuid.UUID = None
    id_client: uuid.UUID = None
    created_at: datetime = None
    updated_at: datetime = None
    status: str = None
    amount: float = None
    amount_vat: float = None

@dataclass
class FailedCreateTransaction(TransactionEvent):
    id_transaction: uuid.UUID = None
    id_client: uuid.UUID = None
    created_at: datetime = None
    status: str = None
    amount: float = None
    amount_vat: float = None

@dataclass
class CanceledTransaction(TransactionEvent):
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

@dataclass
class FailedApprovedTransaction(TransactionEvent):
    id_transaction: uuid.UUID = None
    updated_at: datetime = None