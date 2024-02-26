from dataclasses import dataclass

from pda.seedwork.domain.entities import Entity
from pda.seedwork.domain.factories import Factory
from pda.seedwork.domain.repositories import Mapper
from .entities import Transaction
from .exceptions import ObjectTypeDoesNotExistInPropertiesException
from .rules import PositiveAmount, ValidPayment


@dataclass
class _TransactionFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if isinstance(obj, Entity):
            return mapper.entity_to_dto(obj)
        else:
            transaction: Transaction = mapper.dto_to_entity(obj)

            self.validate_rule(PositiveAmount(transaction.leases))
            [
                self.validate_rule(ValidPayment(payment))
                for lease in transaction.leases
                for payment in lease.payments
            ]

            return transaction


@dataclass
class PropertiesFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if mapper.get_type() == Transaction.__class__:
            transaction_factory = _TransactionFactory()
            return transaction_factory.create_object(obj, mapper)
        else:
            raise ObjectTypeDoesNotExistInPropertiesException()
