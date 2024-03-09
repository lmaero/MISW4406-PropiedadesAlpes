from pda.modules.properties.application.commands.approve_transaction import (
    ApproveTransaction,
)
from pda.modules.properties.application.commands.cancel_transaction import (
    CancelTransaction,
)
from pda.modules.properties.application.commands.create_transaction import (
    CreateTransaction,
)
from pda.modules.properties.domain.events import (
    CreatedTransaction,
    ApprovedTransaction,
    FailedApprovedTransaction,
    FailedCreateTransaction,
)
from pda.modules.sagas.application.commands.payment import (
    PayTransaction,
    ReversePayment,
)
from pda.modules.sagas.domain.events.payment import PaidTransaction, FailedPayment
from pda.seedwork.application.sagas import (
    OrchestrationCoordinator,
    SagaTransaction,
    Start,
    End,
)
from pda.seedwork.domain.events import DomainEvent


class TransactionsCoordinator(OrchestrationCoordinator):
    def init_steps(self):
        self.steps = [
            Start(index=0),
            SagaTransaction(
                index=1,
                command=CreateTransaction,
                event=CreatedTransaction,
                error=FailedCreateTransaction,
                compensation=CancelTransaction,
                successfully=False,
            ),
            SagaTransaction(
                index=2,
                command=PayTransaction,
                event=PaidTransaction,
                error=FailedPayment,
                compensation=ReversePayment,
                successfully=False,
            ),
            SagaTransaction(
                index=3,
                command=ApproveTransaction,
                event=ApprovedTransaction,
                error=FailedApprovedTransaction,
                compensation=CancelTransaction,
                successfully=False,
            ),
            End(index=4),
        ]

    def start(self):
        self.persist_in_saga_log(self.steps[0])

    def finish(self):
        self.persist_in_saga_log(self.steps[-1])

    def persist_in_saga_log(self, msg):
        pass

    def build_command(self, event: DomainEvent, commant_type: type):
        pass


def listen_message(message):
    if isinstance(message, DomainEvent):
        coordinator = TransactionsCoordinator()
        coordinator.process_event(message)
    else:
        raise NotImplementedError("Message is not a domain event")
