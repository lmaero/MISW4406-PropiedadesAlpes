from uuid import UUID

from pda.config.db import db
from pda.modules.tenant.domain.entities import Tenant
from pda.modules.tenant.domain.factories import TenantFactory
from pda.modules.tenant.domain.repositories import (
    TenantsRepository,
    ProvidersRepository,
)
from .dto import Tenant as Tenant_DTO
from .mappers import TenantMapper


class SQLiteProvidersRepository(ProvidersRepository):

    def get_by_id(self, entity_id: UUID) -> Tenant:
        # TODO
        raise NotImplementedError

    def get_all(self) -> list[Tenant]:
        # TODO
        raise NotImplementedError

    def add(self, entity: Tenant):
        # TODO
        raise NotImplementedError

    def update(self, entity: Tenant):
        # TODO
        raise NotImplementedError

    def delete(self, entity_id: UUID):
        # TODO
        raise NotImplementedError


class SQLiteTenantsRepository(TenantsRepository):
    def __init__(self):
        self._tenants_factory: TenantFactory = TenantFactory()

    @property
    def properties_factory(self):
        return self._properties_factory

    def get_by_id(self, entity_id: UUID) -> Tenant:
        transaction_dto = (
            db.session.query(Tenant_DTO).filter_by(id=str(entity_id)).one()
        )
        return self.properties_factory.create_object(
            transaction_dto, TenantMapper()
        )

    def get_all(self) -> list[Tenant]:
        # TODO
        raise NotImplementedError

    def add(self, transaction: Tenant):
        transaction_dto = self.properties_factory.create_object(
            transaction, TenantMapper()
        )
        db.session.add(transaction_dto)

    def update(self, transaction: Tenant):
        # TODO
        raise NotImplementedError

    def delete(self, transaction_id: UUID):
        # TODO
        raise NotImplementedError
