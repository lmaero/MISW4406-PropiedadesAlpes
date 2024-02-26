from dataclasses import dataclass

from pda.modules.properties.domain.repositories import (
    ProvidersRepository,
    TransactionsRepository,
)
from pda.seedwork.domain.exceptions import FactoryException
from pda.seedwork.domain.factories import Factory
from pda.seedwork.domain.repositories import Repository
from .repositories import SQLiteTransactionsRepository, SQLiteProvidersRepository


@dataclass
class RepositoryFactory(Factory):
    def create_object(self, obj: type, mapper: any = None) -> Repository:
        if obj == TransactionsRepository.__class__:
            return SQLiteTransactionsRepository()
        elif obj == ProvidersRepository.__class__:
            return SQLiteProvidersRepository()
        else:
            raise FactoryException()
