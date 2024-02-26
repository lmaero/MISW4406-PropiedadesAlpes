from pda.modules.properties.domain.entidades import Transaction
from pda.modules.properties.domain.objetos_valor import (
    Lease,
    Payment,
)
from pda.seedwork.domain.repositorios import Mapper
from .dto import Lease as LeaseDTO
from .dto import Transaction as TransactionDTO


class TransactionMapper(Mapper):
    _DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def _process_lease_dto(self, leases_dto: list) -> list[Lease]:
        leases_dict = dict()

        for lease in leases_dto:
            amount = lease.amount
            date = lease.date

            leases_dict.setdefault(str(lease.payment_order), Payment(amount, date))

        payments = list()
        for k, payments_dict in leases_dict.items():
            payments.append(payments_dict)

        return [Lease(payments)]

    def _process_lease(self, lease: any) -> list[LeaseDTO]:
        leases = list()

        for i, payment in enumerate(lease.payments):
            lease_dto = LeaseDTO()
            lease_dto.amount = payment.amount
            lease_dto.date = payment.date
            # lease_dto.payment_order = i

            leases.append(lease_dto)

        return leases

    def get_type(self) -> type:
        return Transaction.__class__

    def entity_to_dto(self, entity: Transaction) -> TransactionDTO:
        transaction_dto = TransactionDTO()
        transaction_dto.created_at = entity.created_at
        transaction_dto.updated_at = entity.updated_at
        transaction_dto.id = str(entity.id)

        leases_dto = list()

        for lease in entity.leases:
            leases_dto.extend(self._process_lease(lease))

        transaction_dto.leases = leases_dto

        return transaction_dto

    def dto_to_entity(self, dto: TransactionDTO) -> Transaction:
        transaction = Transaction(dto.id, dto.created_at, dto.updated_at)
        transaction.leases = list()

        leases_dto: list[LeaseDTO] = dto.leases

        transaction.leases.extend(self._process_lease_dto(leases_dto))

        return transaction
