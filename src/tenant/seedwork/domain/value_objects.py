from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ValueObject: ...


class Invoice(ABC, ValueObject):
    @abstractmethod
    def amount(self) -> float: ...

    @abstractmethod
    def date(self) -> datetime: ...


@dataclass(frozen=True)
class Code(ABC, ValueObject):
    code: str


@dataclass(frozen=True)
class Country(ValueObject):
    code: Code
    name: str


@dataclass(frozen=True)
class City(ValueObject):
    country: ValueObject
    Code: Code
    name: str
