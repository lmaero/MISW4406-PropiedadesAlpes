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
    def persist_in_saga_log(self, msg):
        pass

    @abstractmethod
    def build_command(self, event: DomainEvent, command_type: type) -> Command:
        pass

    def publish_command(self, event: DomainEvent, command_type: type):
        command = self.build_command(event, command_type)
        execute_command(command)

    @abstractmethod
    def init_steps(self):
        pass

    @abstractmethod
    def process_event(self, event: DomainEvent):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def finish(self):
        pass


class Step:
    correlation_id: uuid.UUID
    event_date: datetime.datetime
    index: int


@dataclass
class Start(Step):
    index: int = 0


@dataclass
class End(Step):
    pass


@dataclass
class SagaTransaction(Step):
    command: Command
    event: DomainEvent
    error: DomainEvent
    compensation: Command
    successfully: bool


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
        return len(self.steps) - 1

    def process_event(self, event: DomainEvent):
        step, index = self.get_step_given_an_event(event)
        if self.is_last_saga_transaction(index) and not isinstance(event, step.error):
            self.finish()
        elif isinstance(event, step.error):
            self.publish_command(event, self.steps[index - 1].compensation)
        elif isinstance(event, step.event):
            self.publish_command(event, self.steps[index + 1].compensation)
