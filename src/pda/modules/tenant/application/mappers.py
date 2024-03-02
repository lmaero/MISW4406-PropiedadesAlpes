from pda.modules.tenant.domain.entities import Tenant
from pda.seedwork.application.dto import Mapper as AppMap
from pda.seedwork.domain.repositories import Mapper as RepMap
from .dto import TenantDTO

class TenantMapperDTOJson(AppMap):
    def external_to_dto(self, external_data: dict) -> TenantDTO:
        tenant_dto = TenantDTO()
        tenant_dto.name = external_data.get("name")
        tenant_dto.email = external_data.get("email")
        tenant_dto.guarantor_name = external_data.get("guarantor_name")
        return tenant_dto

    def dto_to_external(self, dto: TenantDTO) -> dict:
        return dto.__dict__
    
class TenantMapper(RepMap):
    _DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    def get_type(self) -> type:
        return Tenant.__class__
    
    def entity_to_dto(self, entity: Tenant) -> TenantDTO:
        created_at = entity.created_at.strftime(self._DATE_FORMAT)
        updated_at = entity.updated_at.strftime(self._DATE_FORMAT)
        _id = str(entity.id)
        tenant_dto = TenantDTO(created_at, updated_at, _id, entity.name, entity.email, entity.guarantor_name)
        return tenant_dto

    def dto_to_entity(self, dto: TenantDTO) -> Tenant:
        tenant = Tenant(dto.id, 
                        dto.name, 
                        dto.email, 
                        dto.guarantor_name, 
                        dto.created_at, 
                        dto.updated_at)
        return tenant