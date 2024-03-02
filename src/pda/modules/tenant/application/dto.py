from pda.seedwork.application.dto import DTO
from dataclasses import dataclass, field

@dataclass(frozen=True)
class TenantDTO(DTO):
    name: str = field(default_factory=str)
    email: str = field(default_factory=str)
    guarantor_name: str = field(default_factory=str)
    id: str = field(default_factory=str)
    created_at: str = field(default_factory=str)
    updated_at: str = field(default_factory=str)