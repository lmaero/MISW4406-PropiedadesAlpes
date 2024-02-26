from pda.seedwork.domain.rules import BusinessRule
from .value_objects import Invoice
from .value_objects import Lease


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
