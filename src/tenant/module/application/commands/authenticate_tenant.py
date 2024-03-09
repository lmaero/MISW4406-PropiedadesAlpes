from dataclasses import dataclass

from tenant.seedwork.application.commands import Command, CommandHandler


@dataclass
class CommandAuthenticateTenant(Command):
    email: str
    password: str


class AuthenticateTenantHandler(CommandHandler): ...
