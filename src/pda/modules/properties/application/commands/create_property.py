from dataclasses import dataclass

from aeroalpes.modulos.vuelos.infraestructura.repositorios import \
    RepositorioReservas
from aeroalpes.seedwork.aplicacion.comandos import ejecutar_commando as comando
from aeroalpes.seedwork.infraestructura.uow import UnidadTrabajoPuerto

from pda.modules.properties.application.mappers import PropertyMapper
from pda.modules.properties.domain.entities import Property
from pda.seedwork.application.commands import Command
from .base import CreatePropertyBaseHandler
from ..dto import (
    TenantDTO,
    TransactionDTO,
    LocationDTO,
    AvailabilityDTO,
    SizeDTO,
    PropertyDTO,
)


@dataclass
class CreateProperty(Command):
    id: str
    created_at: str
    updated_at: str
    tenants: list[TenantDTO]
    transactions: list[TransactionDTO]
    location: LocationDTO
    availability: AvailabilityDTO
    size: SizeDTO


class CreatePropertyHandler(CreatePropertyBaseHandler):
    def handle(self, command: CreateProperty):
        property_dto = PropertyDTO(
            id=command.id,
            created_at=command.created_at,
            updated_at=command.updated_at,
            tenants=command.tenants,
            transactions=command.transactions,
            location=command.location,
            availability=command.availability,
            size=command.size,
        )

        property: Property = self.properties_factory.create_object(
            property_dto, PropertyMapper()
        )
        property.crear_reserva(property)

        repositorio = self.repository_factory.create_object(
            RepositorioReservas.__class__
        )

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, property)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CreateProperty)
def execute_create_property(command: CreateProperty):
    handler = CreatePropertyHandler()
    handler.handle(command)
