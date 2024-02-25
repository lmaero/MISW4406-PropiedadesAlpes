from uuid import UUID
from src.pda.config import db
from src.pda.modules.properties.domain.factories import PropertyFactory
from src.pda.modules.properties.domain.repositories import TransactionRepository
from src.pda.modules.properties.infrastructure.mappers import TransactionMapper
from src.pda.seedwork.domain.entities import Transaction
from .dto import Transaction as TransactionDTO


class TransactionRepositorySQLite(TransactionRepository):

    def __init__(self):
        self._property_factory: PropertyFactory = PropertyFactory()

    @property
    def property_factory(self):
        return self._property_factory

    def get_by_id(self, id: UUID) -> Transaction:
        transaction_dto = db.session.query(TransactionDTO).filter_by(id=str(id)).one()
        return self._property_factory.create_object(transaction_dto, TransactionMapper())