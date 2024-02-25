""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass, field
from src.pda.modules.properties.infrastructure.repositories import TransactionRepositorySQLite
from src.pda.seedwork.domain.exceptions import FactoryException
from src.pda.seedwork.domain.factories import Factory
from src.pda.seedwork.domain.repositories import Repository
from src.pda.modules.properties.domain.repositories import TransactionRepository


@dataclass
class RepositoryFactory(Factory):
    def create_object(self, obj: type, mapper: any = None) -> Repository:
        if obj == TransactionRepository.__class__:
            return TransactionRepositorySQLite()
        else:
            raise FactoryException()