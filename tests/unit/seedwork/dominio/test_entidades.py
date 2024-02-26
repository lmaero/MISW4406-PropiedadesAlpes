"""Pruebas para archivo de entidades de Seedwork

En este archivo usted encontrará las diferentes pruebas de validación para los modelos abstractos y reusables del seedwork

"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

import pytest

from pda.seedwork.domain.entities import Entity
from pda.seedwork.domain.exceptions import ImmutableEntityIdException

"""
    Clases de Soporte para validar el seedwork
"""


@dataclass
class EntityPrueba(Entity):
    campo1: str = field(default=None)
    campo2: int = field(default=0)


"""
    Pruebas
"""


def test_entidad_es_implementable():
    # Dada una entidad que hereda de Entidad
    entidadPrueba = EntityPrueba()

    # Cuando los atributos son validos
    entidadPrueba.campo1 = "Campo1"
    entidadPrueba.campo2 = 2

    # Entonces el objeto no debe ser nulo y los atributos son establecidos
    assert entidadPrueba is not None
    assert entidadPrueba.campo1 == "Campo1"
    assert entidadPrueba.campo2 == 2


def test_inicializa_los_atributos_de_entidad():
    # Dada una entidad
    # Sin ningun tipo de parametros
    entidadPrueba = EntityPrueba()

    # Entonces debe inicializar los atributos en la clase padre Entidad
    assert entidadPrueba is not None
    assert entidadPrueba.id is not None and type(entidadPrueba.id) == UUID
    assert (
        entidadPrueba.updated_at is not None
        and type(entidadPrueba.updated_at) == datetime
    )
    assert (
        entidadPrueba.created_at is not None
        and type(entidadPrueba.created_at) == datetime
    )


def test_entidad_tiene_constructor_con_parametros():
    # Dada una entidad
    # Con parametros de entrada en el constructor
    entidadPrueba = EntityPrueba(campo1="Campo1", campo2=2)

    # Entonces debe inicializarlos sin problema
    assert entidadPrueba is not None
    assert entidadPrueba.campo1 == "Campo1"
    assert entidadPrueba.campo2 == 2


def test_entidad_id_es_inmutable():
    with pytest.raises(ImmutableEntityIdException):
        # Dada una entidad
        entidadPrueba = EntityPrueba()

        # Cuando se intenta cambiar el ID ya establecido
        entidadPrueba.id = "Nuevo ID"

        # Entonces debe lanzar una excepción
