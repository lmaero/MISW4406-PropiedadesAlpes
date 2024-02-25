from pda.seedwork.application.queries import QueryHandler
from src.pda.modules.properties.domain.factories import PropertyFactory
from src.pda.modules.properties.infrastructure.factories import RepositoryFactory


class TransactionQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._property_factory: PropertyFactory = PropertyFactory()

    @property
    def repository_factory(self):
        return self._repository_factory
    
    @property
    def property_factory(self):
        return self._property_factory 