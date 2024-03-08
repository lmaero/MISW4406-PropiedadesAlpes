from abc import ABC, abstractmethod
from functools import singledispatch


class Command:
    ...


class CommandHandler(ABC):
    @abstractmethod
    def handle(self, command: Command):
        raise NotImplementedError()


@singledispatch
def execute_command(command):
    raise NotImplementedError(
        f"There is not implementation for type: {type(command).__name__}"
    )
