from __future__ import annotations

from pydantic import BaseModel, EmailStr

from app.domain.schemas.address import Address, AddressCreate, AddressUpdate


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    gender: str | None = None


class UserCreate(UserBase):
    addresses: list[AddressCreate] = []


class UserUpdate(UserBase):
    addresses: list[AddressUpdate] | None = None


class User(UserBase):
    id: int
    addresses: list[Address] = []

    class Config:
        from_attributes = True


