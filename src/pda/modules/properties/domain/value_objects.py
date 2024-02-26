from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from pda.seedwork.domain.value_objects import ValueObject, Invoice


@dataclass(frozen=True)
class Payment(Invoice):
    amount: float
    date: datetime

    def amount(self) -> float:
        return self.amount

    def date(self) -> datetime:
        return self.date


@dataclass(frozen=True)
class Lease(ValueObject):
    payments: list[Payment] = field(default_factory=list)

    @classmethod
    def is_valid(self) -> bool:
        pass
