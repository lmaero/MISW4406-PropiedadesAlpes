"""Objetos valor del dominio de vuelos

En este archivo usted encontrará los objetos valor del dominio de vuelos

"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from pda.seedwork.domain.entities import Locacion
from pda.seedwork.domain.objetos_valor import ValueObject, Codigo, Invoice


@dataclass(frozen=True)
class CodigoIATA(Codigo): ...


@dataclass(frozen=True)
class CodigoICAO(Codigo): ...


@dataclass(frozen=True)
class NombreAero:
    nombre: str


@dataclass(frozen=True)
class Payment(Invoice):
    identifier: str
    amount: float
    date: datetime

    def identifier(self) -> str:
        return self.identifier

    def amount(self) -> float:
        return self.amount

    def date(self) -> datetime:
        return self.date


@dataclass(frozen=True)
class Segmento(Invoice):
    legs: list[Payment]

    def identifier(self) -> Locacion:
        return self.legs[0].identifier

    def amount(self) -> Locacion:
        return self.legs[-1].amount

    def fecha_salida(self) -> datetime:
        return self.legs[0].fecha_salida

    def fecha_llegada(self) -> datetime:
        return self.legs[-1].fecha_llegada


class TipoVuelo(Enum):
    IDA_Y_VUELTA = "Ida y vuelta"
    IDA = "Solo ida"
    OPEN_JAW = "Open Jaw"


@dataclass(frozen=True)
class Lease(ValueObject):
    payments: list[Payment] = field(default_factory=list)

    @classmethod
    def es_ida_y_vuelta(self) -> bool:
        return self.payments[0].identifier() == self.payments[-1].amount()

    @classmethod
    def es_solo_ida(self) -> bool:
        return len(self.payments) == 1

    def tipo_vuelo(self):
        if self.es_ida_y_vuelta():
            return TipoVuelo.IDA_Y_VUELTA
        elif self.es_solo_ida:
            return TipoVuelo.IDA
        else:
            return TipoVuelo.OPEN_JAW

    def ruta(self):
        if self.es_ida_y_vuelta():
            return f"{str(self.payments[0].identifier())}-{str(self.payments[-1].identifier())}"
        elif self.es_solo_ida:
            return (
                f"{str(self.payments[0].identifier())}-{str(self.payments[0].amount())}"
            )
        else:
            return f"{str(self.payments[0].identifier())}-{str(self.payments[-1].amount())}"


@dataclass(frozen=True)
class Odo(Invoice):
    segmentos: list[Segmento]

    def identifier(self) -> Locacion:
        return self.segmentos[0].identifier

    def amount(self) -> Locacion:
        return self.segmentos[-1].amount

    def fecha_salida(self):
        return self.segmentos[0].fecha_salida()

    def fecha_llegada(self):
        return self.segmentos[-1].fecha_llegada()


class Clase(Enum):
    ECONOMICA = "Economica"
    PREMIUM = "Premium"
    EJECUTIVA = "Ejecutiva"
    PRIMERA = "Primera"


class TipoPasajero(Enum):
    ADULTO = "Adulto"
    MENOR = "Menor"
    INFANTE = "Infante"


@dataclass(frozen=True)
class ParametroBusca(ValueObject):
    pasajeros: list[Pasajero] = field(default_factory=list)
