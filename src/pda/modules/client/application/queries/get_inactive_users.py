from pda.seedwork.application.queries import Query, QueryHandler, QueryResult


class GetInactiveUsers(Query):
    status: str


class GetInactiveUsersHandler(QueryHandler):
    def handle(self, query: QueryResult) -> QueryResult:
        pass
