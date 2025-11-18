from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm.session import Session

from app.domain.models import Timezone


class TimezoneRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, tz_id: int) -> Timezone | None:
        return self.db.scalar(select(Timezone).where(Timezone.id == tz_id))

    def find(self, offset: str, description: str) -> Timezone | None:
        return self.db.scalar(
            select(Timezone).where(Timezone.offset == offset, Timezone.description == description)
        )

    def create(self, offset: str, description: str) -> Timezone:
        tz = Timezone(offset=offset, description=description)
        self.db.add(tz)
        self.db.flush()
        return tz
