from __future__ import annotations

from pydantic import BaseModel


class TimezoneCreateSchema(BaseModel):
    offset: str
    description: str


class TimezoneSchema(BaseModel):
    id: int
    offset: str
    description: str

    class Config:
        from_attributes = True
