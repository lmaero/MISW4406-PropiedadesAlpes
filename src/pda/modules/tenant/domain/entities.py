from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from pda.modules.tenant.domain.events import CreatedTenant
from pda.seedwork.domain.entities import RootAggregation

@dataclass
class Tenant(RootAggregation):
    def create_tenant(self, tenant: Tenant):
        self.id = tenant.id
        self.name = tenant.name
        self.email = tenant.email
        self.guarantor_name = tenant.guarantor_name
        self.created_at = tenant.created_at
        self.updated_at = tenant.updated_at
        
        self.add_event(
            CreatedTenant(
                id_tenant=self.id,
                name=self.name,
                email=self.email,
                guarantor_name=self.guarantor_name,
                created_at=self.created_at,
                updated_at=self.updated_at,
            )
        )