import datetime
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from pda.seedwork.application.commands import Command
from pda.seedwork.domain.events import DomainEvent
from .commands import execute_command


class SagaCoordinator(ABC):
    correlation_id: uuid.UUID

    @abstractmethod
    def persist_in_saga_log(self, msg): ...

    @abstractmethod
    def build_command(self, event: DomainEvent, commant_type: type) -> Command: ...

    def publish_command(self, event: DomainEvent, commant_type: type):
        command = self.build_command(event, commant_type)
        execute_command(command)

    @abstractmethod
    def init_steps(self): ...

    @abstractmethod
    def process_event(self, event: DomainEvent): ...

    @abstractmethod
    def start(): ...

    @abstractmethod
    def finish(): ...


class Step:
    correlation_id: uuid.UUID
    event_date: datetime.datetime
    index: int


@dataclass
class Start(Step):
    index: int = 0


@dataclass
class End(Step): ...


@dataclass
class SagaTransaction(Step):
    command: Command
    event: DomainEvent
    error: DomainEvent
    compensation: Command
    successfully: bool


class ChoreographyCoordinator(SagaCoordinator, ABC):
    # TODO Piense como podemos hacer un Coordinador con coreografía y Sagas
    # Piense en como se tiene la clase Transaccion, donde se cuenta con un atributo de compensación
    # ¿Tal vez un manejo de tuplas o diccionarios?
    ...


class OrchestrationCoordinator(SagaCoordinator, ABC):
    steps: list[Step]
    index: int

    def get_step_given_an_event(self, event: DomainEvent):
        for i, step in enumerate(self.steps):
            if not isinstance(step, SagaTransaction):
                continue
            if isinstance(event, step.event) or isinstance(event, step.error):
                return step, i
        raise Exception("Event is not part of the transaction")

    def is_last_saga_transaction(self, index):
        return len(self.pasos) - 1

    def process_event(self, event: DomainEvent):
        step, index = self.get_step_given_an_event(event)
        if self.is_last_saga_transaction(index) and not isinstance(event, step.error):
            self.finish()
        elif isinstance(event, step.error):
            self.publish_command(event, self.step[index - 1].compensation)
        elif isinstance(event, step.event):
            self.publish_command(event, self.steps[index + 1].compensation)
