from dataclasses import dataclass
from pda.modules.tenant.application.mappers import TenantMapper

from pda.modules.tenant.infraestructure.repositories import \
    TenantsRepository
from pda.seedwork.application.queries import Query, QueryResult
from pda.seedwork.application.queries import execute_query as query
from .base import TenantQueryBaseHandler

@dataclass
class GetTenant(Query):
    id: str


class GetTenantHandler(TenantQueryBaseHandler):
    def handle(self, execute_query: GetTenant) -> QueryResult:
        tenant = self.repository_factory.create_object(
            TenantsRepository.__class__
        )
        tenant = self.tenant_factory.create_object(
            tenant.get_by_id(query.id), TenantMapper()
        )
        return QueryResult(result=tenant)


@query.register(GetTenant)
def execute_get_tenant_query(execute_query: GetTenant):
    handler = GetTenantHandler()
    return handler.handle(execute_query)

