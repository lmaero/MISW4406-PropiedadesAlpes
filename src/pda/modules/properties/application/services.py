from pda.modules.properties.domain.entities import Transaction
from pda.modules.properties.domain.factories import PropertiesFactory
from pda.modules.properties.infrastructure.factories import RepositoryFactory
from pda.modules.properties.infrastructure.repositories import TransactionsRepository
from pda.seedwork.application.services import Service
from pda.seedwork.infrastructure.uow import UnitOfWorkPort
from .dto import TransactionDTO
from .mappers import TransactionMapper


class TransactionService(Service):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._properties_factory: PropertiesFactory = PropertiesFactory()

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def properties_factory(self):
        return self._properties_factory

    def create_transaction(self, transaction_dto: TransactionDTO) -> TransactionDTO:
        transaction: Transaction = self.properties_factory.create_object(
            transaction_dto, TransactionMapper()
        )
        transaction.create_transaction(transaction)

        repository = self.repository_factory.create_object(
            TransactionsRepository.__class__
        )

        UnitOfWorkPort.register_batch(repository.add, transaction)
        UnitOfWorkPort.savepoint()
        UnitOfWorkPort.commit()

        return self.properties_factory.create_object(transaction, TransactionMapper())

    def get_transaction_by_id(self, id) -> TransactionDTO:
        repository = self.repository_factory.create_object(
            TransactionsRepository.__class__
        )
        return self.properties_factory.create_object(
            repository.get_by_id(id), TransactionMapper()
        )
