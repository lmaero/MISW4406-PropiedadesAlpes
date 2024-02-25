from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from pda.seedwork.domain.value_objects import ValueObject, Codigo, Ruta, \
    Locacion

@dataclass(frozen=True)
class Payment(ValueObject):
    amount: float
    date: datetime

@dataclass(frozen=True)
class Lease(ValueObject):
    payments: list[Payment] = field(default_factory=list)

#############################
@dataclass(frozen=True)
class Leg(Ruta):
    fecha_salida: datetime
    fecha_llegada: datetime
    origen: Locacion
    destino: Locacion

    def origen(self) -> Locacion:
        return self.origen

    def destino(self) -> Locacion:
        return self.destino

    def fecha_salida(self) -> datetime:
        return self.fecha_salida

    def fecha_llegada(self) -> datetime:
        return self.fecha_llegada


@dataclass(frozen=True)
class Segmento(Ruta):
    legs: list[Leg]

    def origen(self) -> Locacion:
        return self.legs[0].origen

    def destino(self) -> Locacion:
        return self.legs[-1].destino

    def fecha_salida(self) -> datetime:
        return self.legs[0].fecha_salida

    def fecha_llegada(self) -> datetime:
        return self.legs[-1].fecha_llegada


class TipoVuelo(Enum):
    IDA_Y_VUELTA = "Ida y vuelta"
    IDA = "Solo ida"
    OPEN_JAW = "Open Jaw"


@dataclass(frozen=True)
class Tenant(ValueObject):
    odos: list[Odo] = field(default_factory=list)
    # proveedor: 'Proveedor' = field(default_factory='Proveedor')

    @classmethod
    def es_ida_y_vuelta(self) -> bool:
        return self.odos[0].origen() == self.odos[-1].destino()

    @classmethod
    def es_solo_ida(self) -> bool:
        return len(self.odos) == 1

    def tipo_vuelo(self):
        if self.es_ida_y_vuelta():
            return TipoVuelo.IDA_Y_VUELTA
        elif self.es_solo_ida:
            return TipoVuelo.IDA
        else:
            return TipoVuelo.OPEN_JAW

    def ruta(self):
        if self.es_ida_y_vuelta():
            return f"{str(self.odos[0].origen())}-{str(self.odos[-1].origen())}"
        elif self.es_solo_ida:
            return f"{str(self.odos[0].origen())}-{str(self.odos[0].destino())}"
        else:
            return f"{str(self.odos[0].origen())}-{str(self.odos[-1].destino())}"


@dataclass(frozen=True)
class Odo(Ruta):
    segmentos: list[Segmento]

    def origen(self) -> Locacion:
        return self.segmentos[0].origen

    def destino(self) -> Locacion:
        return self.segmentos[-1].destino

    def fecha_salida(self):
        return self.segmentos[0].fecha_salida()

    def fecha_llegada(self):
        return self.segmentos[-1].fecha_llegada()
