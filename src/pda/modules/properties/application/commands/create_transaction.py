from dataclasses import dataclass

from pda.modules.properties.application.dto import LeaseDTO, TransactionDTO
from pda.modules.properties.application.mappers import TransactionMapper
from pda.modules.properties.domain.entities import Transaction
from pda.modules.properties.infrastructure.repositories import (
    TransactionsRepository,
    TransactionsEventsRepository,
)
from pda.seedwork.application.commands import Command
from pda.seedwork.application.commands import execute_command as command
from pda.seedwork.infrastructure.uow import UnitOfWorkPort
from .base import CreateTransactionBaseHandler


@dataclass
class CreateTransaction(Command):
    created_at: str
    updated_at: str
    id: str
    leases: list[LeaseDTO]


class CreateTransactionHandler(CreateTransactionBaseHandler):
    def handle(self, transaction_command: CreateTransaction):
        transaction_dto = TransactionDTO(
            created_at=transaction_command.created_at,
            updated_at=transaction_command.updated_at,
            id=transaction_command.id,
            leases=transaction_command.leases,
        )

        transaction: Transaction = self.properties_factory.create_object(
            transaction_dto, TransactionMapper()
        )
        transaction.create_transaction(transaction)

        repository = self.repository_factory.create_object(TransactionsRepository)
        repository_events = self.repository_factory.create_object(
            TransactionsEventsRepository
        )

        UnitOfWorkPort.register_batch(
            repository.add, transaction, func_repository_events=repository_events.add
        )
        UnitOfWorkPort.commit()


@command.register(CreateTransaction)
def execute_create_transaction_command(execute_command: CreateTransaction):
    handler = CreateTransactionHandler()
    handler.handle(execute_command)
