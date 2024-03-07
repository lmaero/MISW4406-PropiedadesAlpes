from abc import ABC
from tenant.seedwork.domain.repositories import Repository


class TenantRepository(Repository, ABC):
    ...