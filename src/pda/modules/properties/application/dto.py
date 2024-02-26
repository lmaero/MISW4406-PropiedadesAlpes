from dataclasses import dataclass, field

from pda.seedwork.application.dto import DTO


@dataclass(frozen=True)
class PaymentDTO(DTO):
    amount: float
    date: str


@dataclass(frozen=True)
class LeaseDTO(DTO):
    payments: list[PaymentDTO]


@dataclass(frozen=True)
class TransactionDTO(DTO):
    created_at: str = field(default_factory=str)
    updated_at: str = field(default_factory=str)
    id: str = field(default_factory=str)
    leases: list[LeaseDTO] = field(default_factory=list)
