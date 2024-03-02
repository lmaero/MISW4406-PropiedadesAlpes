from pda.modules.properties.infrastructure.dispatchers import Dispatcher
from pda.seedwork.application.handlers import Handler


class TenantIntegrationHandler(Handler):
    @staticmethod
    def created_tenant_handler(event):
        dispatcher = Dispatcher()
        dispatcher.publish_event(event, "tenant-events")

    @staticmethod
    def leased_property_handler(event):
        dispatcher = Dispatcher()
        dispatcher.publish_event(event, "tenant-events")