from pydispatch import dispatcher

from pda.modules.tenant.domain.events import CreatedTenant
from .handlers import TenantIntegrationHandler

dispatcher.connect(
    TenantIntegrationHandler.created_tenant_handler,
    signal=f"{CreatedTenant.__name__}Integration",
)
