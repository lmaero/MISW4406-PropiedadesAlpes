from abc import ABC

from pda.seedwork.application.commands import Command, CommandHandler


class RegisterUser(Command):
    names: str
    last_names: str
    email: str
    password: str
    is_business: bool


class RegisterUserHandler(CommandHandler, ABC):
    pass
