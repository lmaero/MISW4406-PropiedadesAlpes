""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from src.pda.seedwork.domain.repositories import Mapper
from src.pda.modules.properties.domain.value_objects import Lease, Payment
from src.pda.modules.properties.domain.entities import Transaction
from .dto import Leases as LeasesDTO
from .dto import Payment as PaymentDTO
from .dto import Transaction as TransactionDTO

class TransactionMapper(Mapper):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _process_leases_dto(self, leases_dto: list) -> list[Lease]:
        lease_dict = dict()
        
        for les in leases_dto:
            amount = les.amount
            date = les.date
            lease_dict.setdefault(str(les.payment),Payment(amount, date))

        payments = list()
        for k, payments_dict in lease_dict.items():
            payments.append(Payment(payments_dict))

        return Lease(payments)


    def _process_lease(self, lease: any) -> list[LeasesDTO]:
        lease_dtos = list()
        
        for i, pau in enumerate(lease.payments):
            payment_dto = PaymentDTO()
            payment_dto.amount = pau.amount
            payment_dto.date = pau.date
            lease_dtos.append(payment_dto)
        
        return lease_dtos

    def get_type(self) -> type:
        return Transaction.__class__

    def entity_to_dto(self, entitie: Transaction) -> TransactionDTO:

        transaction_dto = TransactionDTO()
        transaction_dto.id = str(entitie.id)
        transaction_dto.currency = entitie.currency

        leases_dto = list()
        for lease in entitie.leases:
            leases_dto.extend(self._process_lease(lease))
        
        transaction_dto.leases = leases_dto

        return transaction_dto

    def dto_to_entity(self, dto: TransactionDTO) -> Transaction:
        transaction = Transaction(dto.id, dto.currency)
        transaction.leases = list()

        leases_dto: list[LeasesDTO] = dto.leases

        transaction.leases.extend(self._process_leases_dto(leases_dto))

        return transaction