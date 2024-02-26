from pda.seedwork.domain.exceptions import FactoryException


class ObjectTypeDoesNotExistInPropertiesException(FactoryException):
    def __init__(
        self,
        message="Factory doesn't exist in the properties module.",
    ):
        self.__message = message

    def __str__(self):
        return str(self.__message)
