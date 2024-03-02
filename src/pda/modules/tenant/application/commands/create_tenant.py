from dataclasses import dataclass
from pda.modules.tenant.application.dto import TenantDTO
from pda.modules.tenant.application.mappers import TenantMapper
from pda.modules.tenant.domain.entities import Tenant
from pda.modules.tenant.infraestructure.repositories import \
    TenantsRepository
from pda.seedwork.application.commands import Command
from pda.seedwork.application.commands import execute_command as command
from pda.seedwork.infrastructure.uow import UnitOfWorkPort
from .base import CreateTenantBaseHandler

@dataclass
class CreateTenant(Command):
    created_at: str
    updated_at: str
    id: str
    name: str
    email: str
    guarantor_name: str

class CreateTenantHandler(CreateTenantBaseHandler):
    def handle(self, command: CreateTenant):
        tenant_dto = TenantDTO(
            created_at=command.created_at,
            updated_at=command.updated_at,
            id=command.id,
            name=command.name,
            email=command.email,
            guarantor_name=command.guarantor_name,
        )

        tenant: Tenant = self.tenant_factory.create_object(
            tenant_dto, TenantMapper()
        )
        tenant.create_tenant(tenant)

        repository = self.repository_factory.create_object(
            TenantsRepository.__class__
        )

        UnitOfWorkPort.register_batch(repository.add, tenant)
        UnitOfWorkPort.savepoint()
        UnitOfWorkPort.commit()

@command.register(CreateTenant)
def execute_create_tenant_command(execute_command: CreateTenant):
    handler = CreateTenantHandler()
    handler.handle(execute_command)