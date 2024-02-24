from dataclasses import dataclass, field
from datetime import datetime

from pda.seedwork.application.dto import DTO


@dataclass(frozen=True)
class CurrencyDTO(DTO):
    symbol: str = field(default_factory=str)
    acronym: str = field(default_factory=str)


@dataclass(frozen=True)
class PaymentDTO(DTO):
    id: str = field(default_factory=str)
    amount: float = field(default_factory=float)
    date: datetime = field(default_factory=str)


@dataclass(frozen=True)
class LeaseDTO(DTO):
    payments: list[PaymentDTO] = field(default_factory=list)


@dataclass(frozen=True)
class TransactionDTO(DTO):
    id: str = field(default_factory=str)
    currency: CurrencyDTO = field(default_factory=str)
    leases: list[LeaseDTO] = field(default_factory=list)
