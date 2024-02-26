from abc import ABC

from pda.seedwork.domain.repositorios import Repository


class TransactionsRepository(Repository, ABC):
    pass


class ProvidersRepository(Repository, ABC):
    pass
