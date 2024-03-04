from abc import ABC

from pda.modules.properties.domain.entities import Transaction
from pda.modules.properties.domain.events import CreatedTransaction, TransactionEvent
from pda.modules.properties.domain.value_objects import (
    Lease,
    Payment,
)
from pda.seedwork.domain.repositories import Mapper
from pda.seedwork.infrastructure.utils import unix_time_millis
from .dto import Lease as LeaseDTO
from .dto import Transaction as TransactionDTO
from .exceptions import MissingFactoryImplementationException


class TransactionEventsMapper(Mapper, ABC):
    versions = ("v1",)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            CreatedTransaction: self._entity_to_created_transaction,
        }

    def get_type(self) -> type:
        return TransactionEvent.__class__

    def is_valid_version(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entity_to_created_transaction(
        self, entity: CreatedTransaction, version=LATEST_VERSION
    ):
        def v1(event):
            from .schema.v1.events import (
                TransactionCreatedPayload,
                CreatedTransactionEvent,
            )

            payload = TransactionCreatedPayload(
                id_transaction=str(entity.id_transaction),
                id_client=str(entity.id_client),
                created_at=int(unix_time_millis(event.created_at)),
            )
            integration_event = CreatedTransactionEvent(id=str(event.id))
            integration_event.id = str(event.id)
            integration_event.time = int(unix_time_millis(event.created_at))
            integration_event.spec_version = str(version)
            integration_event.type = "CreatedTransaction"
            integration_event.data_content_type = "AVRO"
            integration_event.service_name = "pda"
            integration_event.data = payload

            return integration_event

        if not self.is_valid_version(version):
            raise Exception(f"It is not possible to process version: {version}")

        if version == "v1":
            return v1(entity)

    def entity_to_dto(
        self, entity: TransactionEvent, version=LATEST_VERSION
    ) -> TransactionDTO:
        if not entity:
            raise MissingFactoryImplementationException
        func = self.router.get(entity.__class__, None)

        if not func:
            raise MissingFactoryImplementationException

        return func(entity, version=version)

    def dto_to_entity(self, dto: TransactionDTO, version=LATEST_VERSION) -> Transaction:
        raise NotImplementedError


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
