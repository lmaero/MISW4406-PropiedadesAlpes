from dataclasses import dataclass

from pda.modules.tenant.domain.repositories import (
    ProvidersRepository,
    TenantsRepository,
)
from pda.seedwork.domain.exceptions import FactoryException
from pda.seedwork.domain.factories import Factory
from pda.seedwork.domain.repositories import Repository
from .repositories import SQLiteTenantsRepository, SQLiteProvidersRepository


@dataclass
class RepositoryFactory(Factory):
    def create_object(self, obj: type, mapper: any = None) -> Repository:
        if obj == TenantsRepository.__class__:
            return SQLiteTenantsRepository()
        elif obj == ProvidersRepository.__class__:
            return SQLiteProvidersRepository()
        else:
            raise FactoryException()
