from .rules import BusinessRule


class DomainException(Exception):
    pass


class ImmutableEntityIdException(DomainException):
    def __init__(self, message="El identificador debe ser inmutable"):
        self.__message = message

    def __str__(self):
        return str(self.__message)


class BusinessRuleException(DomainException):
    def __init__(self, rule: BusinessRule):
        self.rule = rule

    def __str__(self):
        return str(self.rule)


class FactoryException(DomainException):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return str(self.__message)
