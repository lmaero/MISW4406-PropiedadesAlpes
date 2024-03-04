from abc import ABC
from uuid import UUID

from pulsar.schema import JsonSchema

from pda.config.db import db
from pda.modules.properties.domain.entities import Transaction
from pda.modules.properties.domain.factories import PropertiesFactory
from pda.modules.properties.domain.repositories import (
    TransactionsRepository,
    ProvidersRepository,
    TransactionsEventsRepository,
)
from .dto import Transaction as Transaction_DTO, TransactionEvents
from .mappers import TransactionMapper, TransactionEventsMapper


class SQAlchemyProvidersRepository(ProvidersRepository):
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


class SQAlchemyTransactionsRepository(TransactionsRepository):
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


class SQLAlchemyTransactionEventsRepository(TransactionsEventsRepository, ABC):
    def __init__(self):
        self._properties_factory: PropertiesFactory = PropertiesFactory()

    @property
    def properties_factory(self):
        return self._properties_factory

    def get_by_id(self, id: UUID) -> Transaction:
        transaction_dto = db.session.query(Transaction_DTO).filter_by(id=str(id)).one()
        return self.properties_factory.create_object(
            transaction_dto, TransactionEventsMapper()
        )

    def get_all(self) -> list[Transaction]:
        raise NotImplementedError

    def add(self, event):
        transaction_event = self.properties_factory.create_object(
            event, TransactionEventsMapper()
        )

        parser_payload = JsonSchema(transaction_event.data.__class__)
        json_str = parser_payload.encode(transaction_event.data)

        event_dto = TransactionEvents()
        event_dto.id = str(event.id)
        event_dto.id_entity = str(event.id_transaction)
        event_dto.event_date = event.created_at
        event_dto.version = str(transaction_event.spec_version)
        event_dto.event_type = event.__class__.__name__
        event_dto.content_format = "JSON"
        event_dto.service_name = str(transaction_event.service_name)
        event_dto.content = json_str

        db.session.add(event_dto)

    def update(self, transaction: Transaction):
        raise NotImplementedError

    def delete(self, transaction_id: UUID):
        raise NotImplementedError
