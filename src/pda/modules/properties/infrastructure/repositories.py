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
from .dto import Transaction as Transaction_DTO
from .mappers import TransactionMapper


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
            transaction_dto, MapadeadorEventosReserva()
        )

    def get_all(self) -> list[Transaction]:
        raise NotImplementedError

    def add(self, event):
        transaction_event = self.properties_factory.create_object(
            event, MapadeadorEventosReserva()
        )

        parser_payload = JsonSchema(transaction_event.data.__class__)
        json_str = parser_payload.encode(transaction_event.data)

        # TODO: Change to our entity
        event_dto = EventosReserva()
        event_dto.id = str(event.id)
        event_dto.id_entidad = str(event.id_reserva)
        event_dto.fecha_evento = event.fecha_creacion
        event_dto.version = str(transaction_event.specversion)
        event_dto.tipo_evento = event.__class__.__name__
        event_dto.formato_contenido = "JSON"
        event_dto.nombre_servicio = str(transaction_event.service_name)
        event_dto.contenido = json_str

        db.session.add(event_dto)

    def update(self, transaction: Transaction):
        raise NotImplementedError

    def delete(self, transaction_id: UUID):
        raise NotImplementedError
