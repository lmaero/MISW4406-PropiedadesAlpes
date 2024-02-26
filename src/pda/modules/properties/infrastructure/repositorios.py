""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

from uuid import UUID

from pda.config.db import db
from pda.modules.properties.domain.entidades import Proveedor, Aeropuerto, Transaction
from pda.modules.properties.domain.fabricas import PropertiesFactory
from pda.modules.properties.domain.objetos_valor import (
    NombreAero,
    Odo,
    Payment,
    Segmento,
    Lease,
    CodigoIATA,
)
from pda.modules.properties.domain.repositorios import (
    TransactionsRepository,
    ProvidersRepository,
)
from .dto import Transaction as Transaction_DTO
from .mapeadores import TransactionMapper


class SQLiteProvidersRepository(ProvidersRepository):

    def get_by_id(self, entity_id: UUID) -> Transaction:
        # TODO
        raise NotImplementedError

    def get_all(self) -> list[Transaction]:
        origen = Aeropuerto(codigo="CPT", nombre="Cape Town International")
        destino = Aeropuerto(codigo="JFK", nombre="JFK International Airport")
        legs = [Payment(origen=origen, destino=destino)]
        segmentos = [Segmento(legs)]
        odos = [Odo(segmentos=segmentos)]

        proveedor = Proveedor(
            codigo=CodigoIATA(codigo="AV"), nombre=NombreAero(nombre="Avianca")
        )
        proveedor.itinerarios = [Lease(payments=odos, proveedor=proveedor)]
        return [proveedor]

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
        db.session.commit()

    def update(self, transaction: Transaction):
        # TODO
        raise NotImplementedError

    def delete(self, transaction_id: UUID):
        # TODO
        raise NotImplementedError
