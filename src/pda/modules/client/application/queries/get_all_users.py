from pda.seedwork.application.queries import Query, QueryHandler, QueryResult


class GetAllUsers(Query):
    pass


class GetAllUsersHandler(QueryHandler):
    def handle(self, query: Query) -> QueryResult:
        pass
