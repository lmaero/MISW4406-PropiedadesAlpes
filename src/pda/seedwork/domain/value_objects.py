from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from .entities import Transaction


@dataclass(frozen=True)
class ValueObject:
    pass


@dataclass(frozen=True)
class Size(ABC, ValueObject):
    size: float
    unit: str


@dataclass(frozen=True)
class Availability(ABC, ValueObject):
    is_available: bool


@dataclass(frozen=True)
class Location(ABC, ValueObject):
    id: str
    address: str
    city: str
    state: str
    country: str
    zip_code: str


class Ruta(ABC, ValueObject):
    @abstractmethod
    def origen(self) -> Transaction:
        pass

    @abstractmethod
    def destino(self) -> Transaction:
        pass

    @abstractmethod
    def fecha_salida(self) -> datetime:
        pass

    @abstractmethod
    def fecha_llegada(self) -> datetime:
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
