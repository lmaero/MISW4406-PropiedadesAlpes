class DomainException(Exception):
    ...
class FactoryException(DomainException):
    def __init__(self, msg):
        self.__msg = msg
    def __str__(self):
        return str(self.__msg)