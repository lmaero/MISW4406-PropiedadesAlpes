from tenant.seedwork.application.queries import Query, QueryHandler, QueryResult
import uuid

class GetDeactivatedTenants(Query):
    status: str

class GetDeactivatedTenantsHandler(QueryHandler):

    def handle() -> QueryResult:
        ...