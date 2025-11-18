from __future__ import annotations

from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.domain.models import Timezone
from app.domain.schemas import TimezoneCreateSchema
from app.infrastructure.db.repositories import TimezoneRepository
from app.exceptions import ValidationError


class TimezoneService:
    def __init__(self, db: Session):
        self.repo = TimezoneRepository(db)

    def get_or_create(self, tz: TimezoneCreateSchema) -> Timezone:
        data = tz.model_dump(exclude_unset=True)
        offset = data.get("offset")
        description = data.get("description")
        if not offset and not description:
            raise ValidationError("Timezone offset and description are required")

        existing = self.repo.find(offset=offset, description=description)
        print(existing)
        if existing:
            return existing
        return self.repo.create(offset=offset, description=description)
