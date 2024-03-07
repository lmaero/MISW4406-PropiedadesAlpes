from tenant.seedwork.domain.value_objects import ValueObject, City
from dataclasses import dataclass

@dataclass(frozen=True)
class FullName(ValueObject):
    name: str
    last_name: str

@dataclass(frozen=True)
class Email(ValueObject):
    address: str
    domain: str
    is_bussines: bool

@dataclass(frozen=True)
class IdCard(ValueObject):
    number: int
    city: City

@dataclass(frozen=True)
class Rut(ValueObject):
    number: int
    city: City

class PaymentMethods(ValueObject):
    # TODO
    pass