from uuid import UUID

from pda.config.db import db
from pda.modules.properties.domain.entities import Transaction
from pda.modules.properties.domain.factories import PropertiesFactory
from pda.modules.properties.domain.repositories import (
    TransactionsRepository,
    ProvidersRepository,
)
from .dto import Transaction as Transaction_DTO
from .mappers import TransactionMapper


class SQLiteProvidersRepository(ProvidersRepository):

    def get_by_id(self, entity_id: UUID) -> Transaction:
        # TODO
        raise NotImplementedError

    def get_all(self) -> list[Transaction]:
        # TODO
        raise NotImplementedError

    def add(self, entity: Transaction):
        # TODO
        raise NotImplementedError

    def update(self, entity: Transaction):
        # TODO
        raise NotImplementedError

    def delete(self, entity_id: UUID):
        # TODO
        raise NotImplementedError


class SQLiteTransactionsRepository(TransactionsRepository):
    def __init__(self):
        self._properties_factory: PropertiesFactory = PropertiesFactory()

    @property
    def properties_factory(self):
        return self._properties_factory

    def get_by_id(self, entity_id: UUID) -> Transaction:
        transaction_dto = (
            db.session.query(Transaction_DTO).filter_by(id=str(entity_id)).one()
        )
        return self.properties_factory.create_object(
            transaction_dto, TransactionMapper()
        )

    def get_all(self) -> list[Transaction]:
        # TODO
        raise NotImplementedError

    def add(self, transaction: Transaction):
        transaction_dto = self.properties_factory.create_object(
            transaction, TransactionMapper()
        )
        db.session.add(transaction_dto)

    def update(self, transaction: Transaction):
        # TODO
        raise NotImplementedError

    def delete(self, transaction_id: UUID):
        # TODO
        raise NotImplementedError
