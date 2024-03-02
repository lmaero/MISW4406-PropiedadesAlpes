from pda.seedwork.domain.exceptions import FactoryException


class ObjectTypeDoesNotExistInTenantException(FactoryException):
    def __init__(
        self,
        message="Factory doesn't exist in the tenant module.",
    ):
        self.__message = message

    def __str__(self):
        return str(self.__message)
