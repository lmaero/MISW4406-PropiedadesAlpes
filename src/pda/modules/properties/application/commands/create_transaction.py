from dataclasses import dataclass

from pda.modules.properties.application.dto import LeaseDTO, TransactionDTO
from pda.modules.properties.application.mappers import TransactionMapper
from pda.modules.properties.domain.entities import Transaction
from pda.modules.properties.infrastructure.repositories import \
    TransactionsRepository
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
    def handle(self, comando: CreateTransaction):
        transaction_dto = TransactionDTO(
            created_at=comando.created_at,
            updated_at=comando.updated_at,
            id=comando.id,
            leases=comando.leases,
        )

        transaction: Transaction = self.properties_factory.create_object(
            transaction_dto, TransactionMapper()
        )
        transaction.create_transaction(transaction)

        repository = self.repository_factory.create_object(
            TransactionsRepository.__class__
        )

        UnitOfWorkPort.register_batch(repository.add, transaction)
        UnitOfWorkPort.savepoint()
        UnitOfWorkPort.commit()


@command.register(CreateTransaction)
def execute_create_transaction_command(execute_command: CreateTransaction):
    handler = CreateTransactionHandler()
    handler.handle(execute_command)
