from pda.seedwork.domain.exceptions import FactoryException


class FactoryTypeNotFoundException(FactoryException):
    def __init__(
        self,
        message="There's no factory for the requested type inside this module.",
    ):
        self.__message = message

    def __str__(self):
        return str(self.__message)
