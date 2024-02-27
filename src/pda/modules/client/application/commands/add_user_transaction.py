import uuid

from pda.seedwork.application.commands import Command, CommandHandler


class AddUserTransaction(Command):
    id_user: uuid.UUID
    id_transaction: uuid.UUID


class AddUserTransactionHandler(CommandHandler):
    pass
