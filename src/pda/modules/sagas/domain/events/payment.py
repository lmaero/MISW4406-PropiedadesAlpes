from __future__ import annotations
from dataclasses import dataclass, field
from pda.seedwork.domain.events import (DomainEvent)
from datetime import datetime
import uuid

class PaymentEvent(DomainEvent):
    ...

@dataclass
class PaidTransaction(PaymentEvent):
    transaction_id: uuid.UUID = None
    correlation_id: str = None
    amount: float = None
    amount_vat: float = None
    update_at: datetime = None

@dataclass
class FailedPayment(PaymentEvent):
    transaction_id: uuid.UUID = None
    correlation_id: str = None
    amount: float = None
    amount_vat: float = None
    update_at: datetime = None

@dataclass
class ReversedPayment(PaymentEvent):
    transaction_id: uuid.UUID = None
    correlation_id: str = None
    amount: float = None
    amount_vat: float = None
    update_at: datetime = None