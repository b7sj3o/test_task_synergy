from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.models import Timezone
from app.domain.schemas import TimezoneCreate
from app.infrastructure.db.repositories import TimezoneRepository


class TimezoneService:
    def __init__(self, db: Session):
        self.repo = TimezoneRepository(db)

    def get_or_create(self, tz: TimezoneCreate | None) -> Timezone | None:
        if not tz:
            return None
            
        data = tz.model_dump(exclude_unset=True)
        offset = data.get("offset") or ""
        description = data.get("description") or ""
        if not offset and not description:
            return None
        existing = self.repo.find(offset=offset, description=description)
        if existing:
            return existing
        return self.repo.create(offset=offset, description=description)


