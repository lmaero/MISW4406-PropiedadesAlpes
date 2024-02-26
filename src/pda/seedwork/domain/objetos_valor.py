from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ValueObject:
    pass


@dataclass(frozen=True)
class Codigo(ABC, ValueObject):
    codigo: str


class Invoice(ABC, ValueObject):
    @abstractmethod
    def identifier(self) -> str:
        pass

    @abstractmethod
    def amount(self) -> float:
        pass

    @abstractmethod
    def date(self) -> datetime:
        pass


@dataclass(frozen=True)
class Pais(ValueObject):
    codigo: Codigo
    nombre: str


@dataclass(frozen=True)
class Ciudad(ValueObject):
    pais: Pais
    codigo: Codigo
    nombre: str
