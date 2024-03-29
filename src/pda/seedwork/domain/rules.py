from abc import ABC, abstractmethod


class BusinessRule(ABC):
    __message: str = "Invalid business rule"

    def __init__(self, message):
        self.__message = message

    def message_error(self) -> str:
        return self.__message

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    def __str__(self):
        return f"{self.__class__.__name__} - {self.__message}"


class ImmutableEntityId(BusinessRule):
    entity: object

    def __init__(self, entity, message="Identifier should be immutable"):
        super().__init__(message)
        self.entity = entity

    def is_valid(self) -> bool:
        try:
            if self.entity._id:
                return False
        except AttributeError as error:
            return True
