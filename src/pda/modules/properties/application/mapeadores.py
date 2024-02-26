from datetime import datetime

from pda.modules.properties.domain.entidades import Transaction
from pda.modules.properties.domain.objetos_valor import Lease, Payment
from pda.seedwork.application.dto import Mapper as AppMap
from pda.seedwork.domain.repositorios import Mapper as RepMap
from .dto import TransactionDTO, LeaseDTO, PaymentsDTO


class TransactionMapperDTOJson(AppMap):
    def _process_lease(self, lease: dict) -> LeaseDTO:
        payments_dto: list[PaymentsDTO] = list()

        for payment in lease.get("payments", list()):
            payment_dto: PaymentsDTO = PaymentsDTO(
                payment.get("id"),
                payment.get("amount"),
                payment.get("date"),
            )
            payments_dto.append(payment_dto)

        return LeaseDTO(payments_dto)

    def external_to_dto(self, external_data: dict) -> TransactionDTO:
        transaction_dto = TransactionDTO()

        for lease in external_data.get("leases", list()):
            transaction_dto.leases.append(self._process_lease(lease))

        return transaction_dto

    def dto_to_external(self, dto: TransactionDTO) -> dict:
        return dto.__dict__


class TransactionMapper(RepMap):
    _DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def _process_lease(self, lease_dto: LeaseDTO) -> Lease:
        payments = list()

        for payments_dto in lease_dto.payments:
            identifier = payments_dto.id
            amount = payments_dto.amount
            date = datetime.strptime(payments_dto.date, self._DATE_FORMAT)
            payment: Payment = Payment(identifier, amount, date)
            payments.append(payment)

        return Lease(payments)

    def get_type(self) -> type:
        return Transaction.__class__

    def entity_to_dto(self, entity: Transaction) -> TransactionDTO:
        created_at = entity.created_at.strftime(self._DATE_FORMAT)
        updated_at = entity.updated_at.strftime(self._DATE_FORMAT)
        _id = str(entity.id)

        return TransactionDTO(_id, created_at, updated_at, list())

    def dto_to_entity(self, dto: TransactionDTO) -> Transaction:
        transaction = Transaction()
        transaction.leases = list()

        leases_dto: list[LeaseDTO] = dto.leases

        for lease in leases_dto:
            transaction.leases.append(self._process_lease(lease))

        return transaction
