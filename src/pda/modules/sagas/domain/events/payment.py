from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from pda.seedwork.domain.events import DomainEvent


class PaymentEvent(DomainEvent): ...


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
