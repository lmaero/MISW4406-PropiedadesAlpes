from abc import ABC

from pda.seedwork.application.commands import Command, CommandHandler


class AuthenticateUser(Command):
    email: str
    password: str


class AuthenticateUserHandler(CommandHandler, ABC):
    pass
