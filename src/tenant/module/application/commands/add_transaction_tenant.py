import uuid
from dataclasses import dataclass

from tenant.seedwork.application.commands import Command, CommandHandler


@dataclass
class CommandAddTransactionTenant(Command):
    id_tenant: uuid.UUID
    id_transaction: uuid.UUID


class CommandAddTransactionTenantHandler(CommandHandler): ...
