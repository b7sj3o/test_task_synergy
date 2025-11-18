from __future__ import annotations

from pydantic import BaseModel

from app.domain.schemas.timezone import TimezoneSchema, TimezoneCreateSchema


class AddressCreateSchema(BaseModel):
    street: str
    city: str
    state: str | None = None
    country: str
    postcode: str | None = None
    timezone: TimezoneCreateSchema | None = None


class AddressUpdateSchema(BaseModel):
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postcode: str | None = None
    timezone: TimezoneCreateSchema | None = None


class AddressSchema(BaseModel):
    id: int
    street: str
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postcode: str | None = None
    timezone: TimezoneSchema | None = None

    class Config:
        from_attributes = True
