""" Excepciones para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los Excepciones relacionadas
a la capa de infraestructura del dominio de vuelos

"""

from pda.seedwork.domain.exceptions import FactoryException


class NoExisteImplementacionParaTipoFabricaExcepcion(FactoryException):
    def __init__(
        self,
        message="No existe una implementación para el repositorio con el tipo dado.",
    ):
        self.__mensaje = message

    def __str__(self):
        return str(self.__mensaje)
