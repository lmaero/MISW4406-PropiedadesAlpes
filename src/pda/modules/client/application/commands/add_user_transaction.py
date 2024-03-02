import uuid
from abc import ABC

from pda.seedwork.application.commands import Command, CommandHandler


class AddUserTransaction(Command):
    id_user: uuid.UUID
    id_transaction: uuid.UUID


class AddUserTransactionHandler(CommandHandler, ABC):
    pass
