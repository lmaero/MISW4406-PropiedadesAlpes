from pda.modules.tenant.application.dto import TenantDTO
from pda.modules.tenant.domain.entities import Tenant
from pda.seedwork.domain.repositories import Mapper


class TenantMapper(Mapper):
    _DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def get_type(self) -> type:
        return Tenant.__class__

    def entity_to_dto(self, entity: Tenant) -> TenantDTO:
        tenant_dto = TenantDTO()
        tenant_dto.created_at = entity.created_at
        tenant_dto.updated_at = entity.updated_at
        tenant_dto.id = str(entity.id)
        tenant_dto.name = entity.name
        tenant_dto.email = entity.email
        tenant_dto.guarantor_name = entity.guarantor_name

        return tenant_dto

    def dto_to_entity(self, dto: TenantDTO) -> Tenant:
        tenant = Tenant(dto.id, 
                        dto.name, 
                        dto.email, 
                        dto.guarantor_name, 
                        dto.created_at, 
                        dto.updated_at)
        return tenant
