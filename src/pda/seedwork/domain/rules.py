"""Reglas de negocio reusables parte del seedwork del proyecto

En este archivo usted encontrará reglas de negocio reusables parte del seedwork del proyecto

"""

from abc import ABC, abstractmethod


class BusinessRule(ABC):

    __mensaje: str = "La regla de negocio es invalida"

    def __init__(self, mensaje):
        self.__mensaje = mensaje

    def mensaje_error(self) -> str:
        return self.__mensaje

    @abstractmethod
    def is_valid(self) -> bool: ...

    def __str__(self):
        return f"{self.__class__.__name__} - {self.__mensaje}"


class ImmutableEntityId(BusinessRule):

    entidad: object

    def __init__(
        self, entidad, mensaje="El identificador de la entidad debe ser Inmutable"
    ):
        super().__init__(mensaje)
        self.entidad = entidad

    def is_valid(self) -> bool:
        try:
            if self.entidad._id:
                return False
        except AttributeError as error:
            return True
