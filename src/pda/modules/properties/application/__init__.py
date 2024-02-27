from aeroalpes.modulos.vuelos.dominio.eventos import (
    ReservaCreada,
    ReservaCancelada,
    ReservaAprobada,
    ReservaPagada,
)
from pydispatch import dispatcher

from .handlers import TransactionIntegrationHandler

dispatcher.connect(
    TransactionIntegrationHandler.created_transaction_handler,
    signal=f"{ReservaCreada.__name__}Integracion",
)
dispatcher.connect(
    TransactionIntegrationHandler.handle_reserva_cancelada,
    signal=f"{ReservaCancelada.__name__}Integracion",
)
dispatcher.connect(
    TransactionIntegrationHandler.handle_reserva_pagada,
    signal=f"{ReservaPagada.__name__}Integracion",
)
dispatcher.connect(
    TransactionIntegrationHandler.handle_reserva_aprobada,
    signal=f"{ReservaAprobada.__name__}Integracion",
)
