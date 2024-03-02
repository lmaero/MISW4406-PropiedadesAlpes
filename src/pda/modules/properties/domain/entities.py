from __future__ import annotations

import uuid
from dataclasses import dataclass, field

import pda.modules.properties.domain.value_objects as ov
from pda.modules.properties.domain.events import CreatedTransaction
from pda.seedwork.domain.entities import RootAggregation


@dataclass
class Transaction(RootAggregation):
    id_client: uuid.UUID = field(hash=True, default=None)
    leases: list[ov.Lease] = field(default_factory=list[ov.Lease])

    def create_transaction(self, transaction: Transaction):
        self.id_client = transaction.id_client
        self.created_at = transaction.created_at
        self.updated_at = transaction.updated_at
        self.leases = transaction.leases

        self.add_event(
            CreatedTransaction(
                id=self.id,
                id_client=self.id_client,
                event_date=self.created_at,
            )
        )
