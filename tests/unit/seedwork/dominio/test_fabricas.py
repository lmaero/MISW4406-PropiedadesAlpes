"""Pruebas para archivo de fábrica de Seedwork

En este archivo usted encontrará las diferentes pruebas de validacióm para las fábricas base y reusables definidas en el seedwork

"""

import pytest

from pda.seedwork.domain.fabricas import Factory

"""
    Clases de Soporte para validar el seedwork
"""


class FactoryImplementada(Factory):
    def create_object(self, obj: any, mapper: any) -> any:
        return "Mi Objeto"


class FactorySinImplementar(Factory): ...
"""
    Pruebas
"""


def test_crear_fabrica_sin_implementacion():
    with pytest.raises(TypeError):
        fabrica = FactorySinImplementar()


def test_crear_fabrica_con_implementacion():
    # Dada un nueva fabrica
    fabrica = FactoryImplementada()

    # Con metodo creacional
    assert fabrica.create_object({}, {}) is not None
