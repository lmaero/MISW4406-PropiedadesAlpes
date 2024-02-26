""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from dataclasses import dataclass

from pda.seedwork.domain.entities import Entity
from pda.seedwork.domain.fabricas import Factory
from pda.seedwork.domain.repositorios import Mapper
from .entidades import Transaction
from .excepciones import ObjectTypeDoesNotExistInPropertiesException
from .reglas import PositiveAmount, ValidPayment


@dataclass
class _TransactionFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper = None) -> any:
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
    def create_object(self, obj: any, mapper: Mapper = None) -> any:
        if mapper.get_type() == Transaction.__class__:
            transaction_factory = _TransactionFactory()
            return transaction_factory.create_object(obj, mapper)
        else:
            raise ObjectTypeDoesNotExistInPropertiesException()
