from datetime import datetime

from pda.modules.properties.domain.entities import Transaction
from pda.modules.properties.domain.value_objects import Lease, Payment
from pda.seedwork.application.dto import Mapper as AppMap
from pda.seedwork.domain.repositories import Mapper as RepMap
from .dto import TransactionDTO, LeaseDTO, PaymentDTO


class TransactionMapperDTOJson(AppMap):
    def _process_lease(self, lease: dict) -> LeaseDTO:
        payments_dto: list[PaymentDTO] = list()

        for payment in lease.get("payments", list()):
            payments_dto.append(
                PaymentDTO(
                    payment.get("amount"),
                    payment.get("date"),
                )
            )

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

        for payment_dto in lease_dto.payments:
            amount = payment_dto.amount
            date = datetime.strptime(payment_dto.date, self._DATE_FORMAT)
            payment: Payment = Payment(amount, date)
            payments.append(payment)

        return Lease(payments)

    def get_type(self) -> type:
        return Transaction.__class__

    def entity_to_dto(self, entity: Transaction) -> TransactionDTO:
        created_at = entity.created_at.strftime(self._DATE_FORMAT)
        updated_at = entity.updated_at.strftime(self._DATE_FORMAT)
        _id = str(entity.id)

        return TransactionDTO(created_at, updated_at, _id, list())

    def dto_to_entity(self, dto: TransactionDTO) -> Transaction:
        transaction = Transaction()
        transaction.leases = list()

        leases_dto: list[LeaseDTO] = dto.leases

        for lease in leases_dto:
            transaction.leases.append(self._process_lease(lease))

        return transaction
