from tenant.seedwork.application.commands import Command, CommandHandler
from dataclasses import dataclass

import uuid

@dataclass
class CommandAddTransactionTenant(Command):
    id_tenant: uuid.UUID
    id_transaction: uuid.UUID

class CommandAddTransactionTenantHandler(CommandHandler):
    ...