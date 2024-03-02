from abc import ABC

from pda.modules.tenant.domain.factories import TenantFactory
from pda.modules.tenant.infrastructure.factories import RepositoryFactory
from pda.seedwork.application.queries import QueryHandler


class TenantQueryBaseHandler(QueryHandler, ABC):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._tenant_factory: TenantFactory = TenantFactory()

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def tenant_factory(self):
        return self._tenant_factory
