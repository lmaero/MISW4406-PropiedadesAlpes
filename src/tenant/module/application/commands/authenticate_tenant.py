from tenant.seedwork.application.commands import Command, CommandHandler
from dataclasses import dataclass

@dataclass
class CommandAuthenticateTenant(Command):
    email: str
    password: str

class AuthenticateTenantHandler(CommandHandler):
    ...