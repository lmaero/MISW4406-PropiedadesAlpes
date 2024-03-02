from abc import ABC

from pda.modules.properties.domain.factories import PropertiesFactory
from pda.modules.properties.infrastructure.factories import RepositoryFactory
from pda.seedwork.application.commands import CommandHandler


class CreateTransactionBaseHandler(CommandHandler, ABC):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._properties_factory: PropertiesFactory = PropertiesFactory()

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def properties_factory(self):
        return self._properties_factory
