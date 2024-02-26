"""Pruebas para archivo de mixins de Seedwork

En este archivo usted encontrará las diferentes pruebas de validacióm para los mixins base y reusables definidas en el seedwork

"""

import pytest

from pda.seedwork.domain.exceptions import BusinessRuleException
from pda.seedwork.domain.mixins import ValidateMixinRules

"""
    Clases de Soporte para validar el seedwork
"""


class MiClase(ValidateMixinRules): ...


class ReglaNegocioValida:
    def es_valido(self):
        return True


class ReglaNegocioInvalida:
    def es_valido(self):
        return False


"""
    Pruebas
"""


def test_valida_regla_erronea():
    with pytest.raises(BusinessRuleException):
        # Dado un objeto con regla de negocio invalida
        obj = MiClase()
        regla_negocio = ReglaNegocioInvalida()

        # Cuando es validado
        obj.validate_rule(regla_negocio)

        # Lanza exceoción


def test_valida_regla_valida():
    # Dado un objeto con regla de negocio invalida
    obj = MiClase()
    regla_negocio = ReglaNegocioValida()

    # Cuando es validado
    obj.validate_rule(regla_negocio)

    # Llega hasta el final de la operación
    assert True
