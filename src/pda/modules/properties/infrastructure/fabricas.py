from dataclasses import dataclass

from pda.modules.properties.domain.repositorios import (
    ProvidersRepository,
    TransactionsRepository,
)
from pda.seedwork.domain.fabricas import Factory
from pda.seedwork.domain.repositorios import Repository
from .excepciones import FactoryException
from .repositorios import SQLiteTransactionsRepository, \
    SQLiteProvidersRepository


@dataclass
class RepositoryFactory(Factory):
    def create_object(self, obj: type, mapper: any = None) -> Repository:
        if obj == TransactionsRepository.__class__:
            return SQLiteTransactionsRepository()
        elif obj == ProvidersRepository.__class__:
            return SQLiteProvidersRepository()
        else:
            raise FactoryException(message="Factory exception")
