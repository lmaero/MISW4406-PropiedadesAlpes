from tenant.seedwork.application.queries import Query, QueryHandler, QueryResult
import uuid

class GetAllTenants(Query):
    ...

class GetAllTenantsHandler(QueryHandler):

    def handle() -> QueryResult:
        ...