from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class DTO:
    pass


class Mapper(ABC):
    @abstractmethod
    def external_to_dto(self, external_data: any) -> DTO:
        pass

    @abstractmethod
    def dto_to_external(self, dto: DTO) -> any:
        pass
