from pda.seedwork.domain.exceptions import FactoryException


class MissingFactoryImplementationException(FactoryException):
    def __init__(
        self,
        message="There's no implementation for the repository of the given type",
    ):
        self.__message = message

    def __str__(self):
        return str(self.__message)
