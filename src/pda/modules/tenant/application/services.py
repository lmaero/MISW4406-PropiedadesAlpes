from pda.modules.tenant.domain.entities import Tenant
from pda.modules.tenant.domain.factories import TenantFactory
from pda.modules.tenant.infraestructure.factories import RepositoryFactory
from pda.modules.tenant.infraestructure.repositories import TenantRepository
from pda.seedwork.application.services import Service
from pda.seedwork.infrastructure.uow import UnitOfWorkPort
from .dto import TenantDTO
from .mappers import TenantMapper


class TenantService(Service):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._tenant_factory: TenantFactory = TenantFactory()

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def tenant_factory(self):
        return self._tenant_factory

    def create_tenant(self, tenant_dto: TenantDTO) -> TenantDTO:
        tenant: Tenant = self.tenant_factory.create_object(
            tenant_dto, TenantMapper()
        )
        tenant.create_tenant(tenant)

        repository = self.repository_factory.create_object(
            TenantRepository.__class__
        )

        UnitOfWorkPort.register_batch(repository.add, tenant)
        UnitOfWorkPort.savepoint()
        UnitOfWorkPort.commit()

        return self.tenant_factory.create_object(tenant, TenantMapper())
        

    def get_tenant_by_id(self, id) -> TenantDTO:
        repository = self.repository_factory.create_object(
            TenantRepository.__class__
        )
        return self.tenant_factory.create_object(
            repository.get_by_id(id), TenantMapper()
        )
