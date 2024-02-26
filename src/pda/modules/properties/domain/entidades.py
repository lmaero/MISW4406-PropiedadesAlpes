"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de vuelos

"""

from __future__ import annotations

from dataclasses import dataclass, field

import pda.modules.properties.domain.objetos_valor as ov
from pda.seedwork.domain.entities import Locacion, RootAggregation, Entity


@dataclass
class Aeropuerto(Locacion):
    codigo: ov.Codigo = field(default_factory=ov.Codigo)
    nombre: ov.NombreAero = field(default_factory=ov.NombreAero)

    def __str__(self) -> str:
        return self.codigo.codigo.upper()


@dataclass
class Proveedor(Entity):
    codigo: ov.Codigo = field(default_factory=ov.Codigo)
    nombre: ov.NombreAero = field(default_factory=ov.NombreAero)
    itinerarios: list[ov.Lease] = field(default_factory=list[ov.Lease])

    def obtener_itinerarios(self, odos: list[Odo], parametros: ParametroBusca):
        return self.itinerarios


@dataclass
class Pasajero(Entity):
    clase: ov.Clase = field(default_factory=ov.Clase)
    tipo: ov.TipoPasajero = field(default_factory=ov.TipoPasajero)


@dataclass
class Transaction(RootAggregation):
    leases: list[ov.Lease] = field(default_factory=list[ov.Lease])
