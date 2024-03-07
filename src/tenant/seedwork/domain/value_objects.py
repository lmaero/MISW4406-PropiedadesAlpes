from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ValueObject:
    pass


class Invoice(ABC, ValueObject):
    @abstractmethod
    def amount(self) -> float:
        pass

    @abstractmethod
    def date(self) -> datetime:
        pass
