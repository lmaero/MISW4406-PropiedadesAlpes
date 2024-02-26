from pda.seedwork.domain.rules import BusinessRule
from .entidades import Pasajero
from .objetos_valor import Invoice
from .objetos_valor import TipoPasajero, Lease


class MinimoUnAdulto(BusinessRule):

    pasajeros: list[Pasajero]

    def __init__(
        self, pasajeros, mensaje="Al menos un adulto debe ser parte del itinerario"
    ):
        super().__init__(mensaje)
        self.pasajeros = pasajeros

    def is_valid(self) -> bool:
        for pasajero in self.pasajeros:
            if pasajero.tipo == TipoPasajero.ADULTO:
                return True
        return False


class ValidPayment(BusinessRule):
    invoice: Invoice

    def __init__(self, invoice, message="Invoice is invalid"):
        super().__init__(message)
        self.invoice = invoice

    def is_valid(self) -> bool:
        return True


class PositiveAmount(BusinessRule):
    leases: list[Lease]

    def __init__(
        self,
        leases,
        message="Leases list should have at least one lease",
    ):
        super().__init__(message)
        self.leases = leases

    def is_valid(self) -> bool:
        return len(self.leases) > 0 and isinstance(self.leases[0], Lease)
