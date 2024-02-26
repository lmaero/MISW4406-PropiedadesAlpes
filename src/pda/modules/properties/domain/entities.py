from __future__ import annotations

from dataclasses import dataclass, field

import pda.modules.properties.domain.value_objects as ov
from pda.seedwork.domain.entities import RootAggregation


@dataclass
class Transaction(RootAggregation):
    leases: list[ov.Lease] = field(default_factory=list[ov.Lease])
