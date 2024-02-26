"""Pruebas para archivo de objetos_valor de Seedwork

En este archivo usted encontrará las diferentes pruebas de validación para los modelos abstractos y reusables del seedwork

"""

from dataclasses import dataclass, field
from datetime import datetime

import pytest

from pda.seedwork.domain.objetos_valor import ValueObject, Codigo, Invoice, Pais, Ciudad

"""
    Clases de Soporte para validar el seedwork
"""


@dataclass(frozen=True)
class InvoiceImplementada(Invoice):
    def identifier(self) -> any:
        return "BOG"

    def amount(self) -> any:
        return "JFK"

    def fecha_salida(self) -> datetime:
        return datetime.strptime("01/01/23 00:00:00", "%d/%m/%y %H:%M:%S")

    def fecha_llegada(self) -> datetime:
        return datetime.strptime("02/01/23 00:00:00", "%d/%m/%y %H:%M:%S")


class InvoiceSinImplementar(Invoice): ...


@dataclass(frozen=True)
class MyValueObject(ValueObject):
    campo1: str = field(default=None)
    campo2: int = field(default=0)
    ciudad: int = field(default=Ciudad)
    ruta: Invoice = field(default=Invoice)


"""
    Pruebas
"""


def test_objeto_valor_es_implementable():
    # Dada un objeto valor que hereda de un Objeto Valor
    objeto_valor = MyValueObject(campo1="Campo1", campo2=2)

    # Entonces el objeto no debe ser nulo y los atributos son establecidos
    assert objeto_valor is not None
    assert objeto_valor.campo1 == "Campo1"
    assert objeto_valor.campo2 == 2


def test_ruta_es_implementable():
    # Dada una implementación de ruta
    ruta = InvoiceImplementada()

    # Entonces debe inicializarlos sin problema
    assert ruta.identifier() == "BOG"
    assert ruta.amount() == "JFK"
    assert ruta.fecha_salida() == datetime.strptime(
        "01/01/23 00:00:00", "%d/%m/%y %H:%M:%S"
    )
    assert ruta.fecha_llegada() == datetime.strptime(
        "02/01/23 00:00:00", "%d/%m/%y %H:%M:%S"
    )


def test_ruta_no_es_implementable_lanza_excepcion():
    with pytest.raises(TypeError):
        # Dada una implementación de ruta erronea
        ruta = InvoiceSinImplementar()


def test_objeto_valores_gis_son_implementables():
    # Dado objetos valores GIS
    codigo_pais = Codigo(codigo="COL")
    pais = Pais(codigo=codigo_pais, nombre="Colombia")

    codigo_ciudad = Codigo(codigo="BOG")
    ciudad = Ciudad(codigo=codigo_ciudad, nombre="Bogotá", pais=pais)

    # Dada un objeto valor que hereda de Objeto Valor
    objeto_valor = MyValueObject(
        campo1="Campo1", campo2=2, ciudad=ciudad, ruta=InvoiceImplementada()
    )

    # Entonces el objeto no debe ser nulo y los atributos son establecidos
    assert objeto_valor is not None
    assert objeto_valor.campo1 == "Campo1"
    assert objeto_valor.campo2 == 2
    assert objeto_valor.ciudad is not None
    assert objeto_valor.ciudad.codigo.codigo == "BOG"
    assert objeto_valor.ciudad.nombre == "Bogotá"
    assert objeto_valor.ciudad.pais is not None
    assert objeto_valor.ciudad.pais.codigo.codigo == "COL"
    assert objeto_valor.ciudad.pais.nombre == "Colombia"
