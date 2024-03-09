from pda.seedwork.application.sagas import (
    OrchestrationCoordinator,
    SagaTransaction,
    Start,
    End,
)
from pda.seedwork.domain.events import DomainEvent

from pda.modules.sagas.application.commands.payment import (
    PayTransaction,
    ReversePayment,
)

from pda.modules.properties.application.commands.create_transaction import (
    CreateTransaction,
)
from pda.modules.properties.application.commands.approve_transaction import (
    ApproveTransaction,
)
from pda.modules.properties.application.commands.cancel_transaction import (
    CancelTransaction,
)
from pda.modules.properties.domain.events import (
    CreatedTransaction,
    ApprovedTransaction,
    FailedApprovedTransaction,
    FailedCreateTransaction,
)
from pda.modules.sagas.domain.events.payment import PaidTransaction, FailedPayment


class TransactionCoordinator(OrchestrationCoordinator):

    def init_steps(self):
        self.steps = [
            # Inicio(index=0),
            # Transaccion(index=1, comando=CrearReserva, evento=ReservaCreada, error=CreacionReservaFallida, compensacion=CancelarReserva),
            # Transaccion(index=2, comando=PagarReserva, evento=ReservaPagada, error=PagoFallido, compensacion=RevertirPago),
            # Transaccion(index=3, comando=ConfirmarReserva, evento=ReservaGDSConfirmada, error=ConfirmacionFallida, compensacion=ConfirmacionGDSRevertida),
            # Transaccion(index=4, comando=AprobarReserva, evento=ReservaAprobada, error=AprobacionReservaFallida, compensacion=CancelarReserva),
            # Fin(index=5)
            Start(index=0),
            SagaTransaction(
                index=1,
                command=CreateTransaction,
                event=CreatedTransaction,
                error=FailedCreateTransaction,
                compensation=CancelTransaction,
            ),
            SagaTransaction(
                index=2,
                command=PayTransaction,
                event=PaidTransaction,
                error=FailedPayment,
                compensation=ReversePayment,
            ),
            SagaTransaction(
                index=3,
                command=ApproveTransaction,
                event=ApprovedTransaction,
                error=FailedApprovedTransaction,
                compensation=CancelTransaction,
            ),
            End(index=3),
        ]

    def start(self):
        self.persist_in_saga_log(self.steps[0])

    def finish(self):
        self.persist_in_saga_log(self.steps[-1])

    def persist_in_saga_log(self, msg):
        # TODO Persistir estado en DB
        # Probablemente usted podría usar un repositorio para ello
        ...

    def build_command(self, event: DomainEvent, commant_type: type):
        # TODO Transforma un evento en la entrada de un comando
        # Por ejemplo si el evento que llega es ReservaCreada y el tipo_comando es PagarReserva
        # Debemos usar los atributos de ReservaCreada para crear el comando PagarReserva
        ...
