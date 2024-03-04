from abc import ABC, abstractmethod
from functools import singledispatch


class Projection(ABC):
    @abstractmethod
    def execute(self): ...


class ProjectionHandler(ABC):
    @abstractmethod
    def handle(self, projection: Projection): ...


@singledispatch
def execute_projection(projection):
    raise NotImplementedError(
        f"There's no implementation for the projection type: {type(projection).__name__}"
    )
