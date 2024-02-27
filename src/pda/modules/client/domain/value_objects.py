from dataclasses import dataclass

from pda.seedwork.domain.value_objects import ValueObject


@dataclass(frozen=True)
class Name(ValueObject):
    names: str
    last_names: str


@dataclass(frozen=True)
class Email(ValueObject):
    address: str
    domain: str
    is_business: bool


@dataclass(frozen=True)
class NationalID(ValueObject):
    number: int


@dataclass(frozen=True)
class Rut(ValueObject):
    number: int


class PaymentMethods(ValueObject):
    pass
