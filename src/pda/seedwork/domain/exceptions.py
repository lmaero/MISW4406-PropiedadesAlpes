from .rules import BusinessRule


class DomainException(Exception):
    pass


class ImmutableIdException(DomainException):
    def __init__(self, message="ID should be immutable"):
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
