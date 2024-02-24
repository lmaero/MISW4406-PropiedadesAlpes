from abc import ABC, abstractmethod
from uuid import UUID

from .entities import Entity


class Repository(ABC):
    @abstractmethod
    def get_entity_by_id(self, identifier: UUID) -> Entity:
        pass

    @abstractmethod
    def get_all(self) -> list[Entity]:
        pass

    @abstractmethod
    def add(self, entity: Entity):
        pass

    @abstractmethod
    def update(self, entity: Entity):
        pass

    @abstractmethod
    def delete(self, entity_id: UUID):
        pass


class Mapper(ABC):
    @abstractmethod
    def get_type(self) -> type:
        pass

    @abstractmethod
    def entity_to_dto(self, entity: Entity) -> any:
        pass

    @abstractmethod
    def dto_to_entity(self, dto: any) -> Entity:
        pass
