from dataclasses import dataclass

from pda.modules.properties.domain.entities import Transaction
from pda.modules.properties.domain.repositories import (
    TransactionsRepository,
    ProvidersRepository,
    TransactionsEventsRepository,
)
from pda.seedwork.domain.exceptions import FactoryException
from pda.seedwork.domain.factories import Factory
from pda.seedwork.domain.repositories import Repository
from pda.seedwork.infrastructure.views import View
from .repositories import (
    SQLAlchemyTransactionEventsRepository,
    SQAlchemyTransactionsRepository,
    SQAlchemyProvidersRepository,
)
from .views import TransactionView


@dataclass
class RepositoryFactory(Factory):
    def create_object(self, obj: type, mapper: any = None) -> Repository:
        if obj == TransactionsRepository:
            return SQAlchemyTransactionsRepository()
        elif obj == ProvidersRepository:
            return SQAlchemyProvidersRepository()
        elif obj == TransactionsEventsRepository:
            return SQLAlchemyTransactionEventsRepository()
        else:
            raise FactoryException(f"There's no factory for the object: {obj}")


@dataclass
class ViewFactory(Factory):
    def create_object(self, obj: type, mapper: any = None) -> View:
        if obj == Transaction:
            return TransactionView()
        else:
            raise FactoryException(f"There's no factory for the object: {obj}")
