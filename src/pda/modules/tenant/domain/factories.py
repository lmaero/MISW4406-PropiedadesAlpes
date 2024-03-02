from dataclasses import dataclass

from pda.seedwork.domain.entities import Entity
from pda.seedwork.domain.factories import Factory
from pda.seedwork.domain.repositories import Mapper
from pda.modules.tenant.domain.exceptions import ObjectTypeDoesNotExistInTenantException

from .entities import Tenant

@dataclass
class _PrivateTenantFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if isinstance(obj, Entity):
            return mapper.entity_to_dto(obj)
        else:
            tenant: Tenant = mapper.dto_to_entity(obj)
            return tenant

@dataclass
class TenantFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if mapper.get_type() == Tenant.__class__:
            tenant_factory = _PrivateTenantFactory()
            return tenant_factory.create_object(obj, mapper)
        else:
            raise ObjectTypeDoesNotExistInTenantException()        
