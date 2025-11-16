from __future__ import annotations

from pydantic import BaseModel

from app.domain.schemas.timezone import Timezone, TimezoneCreate


class AddressCreate(BaseModel):
    street: str
    city: str
    state: str | None = None
    country: str
    postcode: str | None = None
    timezone: TimezoneCreate | None = None


class AddressUpdate(BaseModel):
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postcode: str | None = None
    timezone: TimezoneCreate | None = None


class Address(BaseModel):
    id: int
    street: str
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postcode: str | None = None
    timezone: Timezone | None = None

    class Config:
        from_attributes = True


