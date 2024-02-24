from functools import singledispatch
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Query(ABC):
    ...

@dataclass
class QueryResponse:
    result: None

class QueryHandler(ABC):
    @abstractmethod
    def handle(self, query: Query) -> QueryResponse:
        raise NotImplementedError()

@singledispatch
def exec_query(query):
    raise NotImplementedError(f'Query type {type(query).__name__} is not implemented')