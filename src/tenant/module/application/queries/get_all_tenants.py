from tenant.seedwork.application.queries import Query, QueryHandler, QueryResult


class GetAllTenants(Query): ...


class GetAllTenantsHandler(QueryHandler):

    def handle() -> QueryResult: ...
