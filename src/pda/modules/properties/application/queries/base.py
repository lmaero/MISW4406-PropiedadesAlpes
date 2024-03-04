from abc import ABC

from pda.modules.properties.domain.factories import PropertiesFactory
from pda.modules.properties.infrastructure.factories import ViewFactory
from pda.seedwork.application.queries import QueryHandler


class TransactionQueryBaseHandler(QueryHandler, ABC):
    def __init__(self):
        self._view_factory: ViewFactory = ViewFactory()
        self._properties_factory: PropertiesFactory = PropertiesFactory()

    @property
    def view_factory(self):
        return self._view_factory

    @property
    def properties_factory(self):
        return self._properties_factory
