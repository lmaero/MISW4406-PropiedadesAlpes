from dataclasses import dataclass, field
from datetime import datetime

from pda.seedwork.application.dto import DTO


@dataclass(frozen=True)
class PaymentsDTO(DTO):
    id: str = field(default_factory=str)
    amount: float = field(default_factory=float)
    date: str = field(default_factory=str)


@dataclass(frozen=True)
class LeaseDTO(DTO):
    payments: list[PaymentsDTO]


@dataclass(frozen=True)
class TransactionDTO(DTO):
    id: str = field(default_factory=str)
    created_at: str = field(default_factory=datetime.now)
    updated_at: str = field(default_factory=datetime.now)
    leases: list[LeaseDTO] = field(default_factory=list)
