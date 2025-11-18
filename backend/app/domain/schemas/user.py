from __future__ import annotations

from pydantic import BaseModel, EmailStr

from app.domain.schemas.address import AddressSchema, AddressCreateSchema, AddressUpdateSchema


class UserBaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    gender: str | None = None


class UserCreateSchema(UserBaseSchema):
    addresses: list[AddressCreateSchema] = []


class UserUpdateSchema(UserBaseSchema):
    addresses: list[AddressUpdateSchema] | None = None


class UserSchema(UserBaseSchema):
    id: int
    addresses: list[AddressSchema] = []

    class Config:
        from_attributes = True
