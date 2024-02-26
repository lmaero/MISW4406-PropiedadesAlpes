"""Objetos valor del dominio de cliente

En este archivo usted encontrará los objetos valor del dominio de cliente

"""

from dataclasses import dataclass

from pda.seedwork.domain.objetos_valor import ValueObject, Ciudad


@dataclass(frozen=True)
class Nombre(ValueObject):
    nombres: str
    apellidos: str


@dataclass(frozen=True)
class Email(ValueObject):
    address: str
    dominio: str
    es_empresarial: bool


@dataclass(frozen=True)
class Cedula(ValueObject):
    numero: int
    ciudad: Ciudad


@dataclass(frozen=True)
class Rut(ValueObject):
    numero: int
    ciudad: Ciudad


class MetodosPago(ValueObject):
    # TODO
    ...
