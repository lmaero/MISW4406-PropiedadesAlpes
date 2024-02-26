from pda.modules.properties.domain.entidades import Transaction
from pda.modules.properties.domain.fabricas import PropertiesFactory
from pda.modules.properties.infrastructure.fabricas import RepositoryFactory
from pda.modules.properties.infrastructure.repositorios import TransactionsRepository
from pda.seedwork.application.servicios import Service
from .dto import TransactionDTO
from .mapeadores import TransactionMapper


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

        repository = self.repository_factory.create_object(
            TransactionsRepository.__class__
        )
        repository.add(transaction)

        return self.properties_factory.create_object(transaction, TransactionMapper())

    def get_transaction_by_id(self, id) -> TransactionDTO:
        repository = self.repository_factory.create_object(
            TransactionsRepository.__class__
        )
        return repository.get_by_id(id).__dict__
