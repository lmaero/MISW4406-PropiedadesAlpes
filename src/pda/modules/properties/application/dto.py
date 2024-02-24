from dataclasses import dataclass, field
from enum import Enum

from pda.seedwork.application.dto import DTO


class ETenantType(Enum):
    INVESTMENT_GROUP = 1
    LAW_FIRM = 2
    CONSULTING_AGENCY = 3
    PROFICIENT = 4
    GOV_INSTITUTION = 5
    FINANCIAL_INSTITUTION = 6


@dataclass(frozen=True)
class SizeDTO(DTO):
    size: float = field(default_factory=float)
    unit: str = field(default_factory=str)


@dataclass(frozen=True)
class AvailabilityDTO(DTO):
    is_available: bool = field(default_factory=bool)


@dataclass(frozen=True)
class LocationDTO(DTO):
    id: str = field(default_factory=str)
    address: str = field(default_factory=str)
    city: str = field(default_factory=str)
    state: str = field(default_factory=str)
    country: str = field(default_factory=str)
    zip_code: str = field(default_factory=str)


@dataclass(frozen=True)
class TenantDTO(DTO):
    id: str = field(default_factory=str)
    company_id: str = field(default_factory=str)
    type: ETenantType = field(default_factory=int)


@dataclass(frozen=True)
class CurrencyDTO(DTO):
    symbol: str = field(default_factory=str)
    acronym: str = field(default_factory=str)


@dataclass(frozen=True)
class TransactionDTO(DTO):
    id: str = field(default_factory=str)
    currency: CurrencyDTO = field(default_factory=str)


@dataclass(frozen=True)
class PropertyDTO(DTO):
    id: str = field(default_factory=str)
    created_at: str = field(default_factory=str)
    updated_at: str = field(default_factory=str)
    tenants: list[TenantDTO] = field(default_factory=list)
    transactions: list[TransactionDTO] = field(default_factory=list)
    location: LocationDTO = field(default_factory=dict)
    availability: AvailabilityDTO = field(default_factory=bool)
    size: SizeDTO = field(default_factory=str)
