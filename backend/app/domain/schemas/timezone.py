from __future__ import annotations

from pydantic import BaseModel


class TimezoneCreate(BaseModel):
    offset: str
    description: str


class Timezone(BaseModel):
    id: int
    offset: str
    description: str

    class Config:
        from_attributes = True


