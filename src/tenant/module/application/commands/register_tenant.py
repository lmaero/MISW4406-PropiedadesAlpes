import datetime
from dataclasses import dataclass

from tenant.module.domain.entities import Tenant, NaturalTenant, BussinesTenant
from tenant.module.domain.value_object import Email, FullName
from tenant.seedwork.application.commands import Command, CommandHandler
from tenant.seedwork.application.commands import execute_command as command


@dataclass
class CommandRegisterTenant(Command):
    name: str
    last_name: str
    email: str
    password: str
    is_bussines: bool


class RegisterTenantHandler(CommandHandler):

    def a_entity(self, command: CommandRegisterTenant) -> Tenant:
        params = dict(
            name=FullName(command.name, command.last_name),
            email=Email(command.email, None, command.is_bussines),
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )

        if command.is_bussines:
            tenant = BussinesTenant(**params)
        else:
            tenant = NaturalTenant(**params)

        return tenant

    def handle(self, command: CommandRegisterTenant):

        tenant = self.a_entity(command)


@command.register(CommandRegisterTenant)
def execute_command_register_tenant(command: CommandRegisterTenant):
    handler = RegisterTenantHandler()
    handler.handle(command)
