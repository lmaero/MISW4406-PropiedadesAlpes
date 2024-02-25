from uuid import UUID
from src.pda.modules.properties.domain.factories import PropertyFactory
from src.pda.modules.properties.domain.repositories import TransactionRepository


class TransactionRepositorySQLite(TransactionRepository):

    def __init__(self):
        self._property_factory: PropertyFactory = PropertyFactory()

    @property
    def fabrica_vuelos(self):
        return self._fabrica_vuelos

    def get_by_id(self, id: UUID) -> Reserva:
        reserva_dto = db.session.query(ReservaDTO).filter_by(id=str(id)).one()
        return self.fabrica_vuelos.crear_objeto(reserva_dto, MapeadorReserva())

    def obtener_todos(self) -> list[Reserva]:
        # TODO
        raise NotImplementedError

    def agregar(self, reserva: Reserva):
        reserva_dto = self.fabrica_vuelos.crear_objeto(reserva, MapeadorReserva())
        db.session.add(reserva_dto)

    def actualizar(self, reserva: Reserva):
        # TODO
        raise NotImplementedError

    def eliminar(self, reserva_id: UUID):
        # TODO
        raise NotImplementedError