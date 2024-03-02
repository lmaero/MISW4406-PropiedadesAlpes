from abc import ABC

from pda.seedwork.domain.repositories import Repository


class TenantsRepository(Repository, ABC):
    pass


class ProvidersRepository(Repository, ABC):
    pass
