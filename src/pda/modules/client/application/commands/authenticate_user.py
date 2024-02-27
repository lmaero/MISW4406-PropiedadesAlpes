from pda.seedwork.application.commands import Command, CommandHandler


class AuthenticateUser(Command):
    email: str
    password: str


class AuthenticateUserHandler(CommandHandler):
    pass
