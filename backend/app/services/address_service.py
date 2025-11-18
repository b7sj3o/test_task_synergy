from __future__ import annotations

from typing import Iterable
from sqlalchemy.orm import Session

from app.domain.models import Address
from app.services.timezone_service import TimezoneService
from app.domain.schemas import AddressCreateSchema, AddressUpdateSchema, TimezoneCreateSchema
from app.infrastructure.db.repositories import AddressRepository


class AddressService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AddressRepository(db)
        self.tz_service = TimezoneService(db)

    def attach_to_user(self, user_id: int, items: Iterable[AddressCreateSchema]) -> None:
        for payload in items:
            data = payload.model_dump(exclude_unset=True)
            tz = self.tz_service.get_or_create(TimezoneCreateSchema(**data.get("timezone")))

            if "timezone" in data:
                del data["timezone"]
            addr = Address(user_id=user_id, **data)

            if tz:
                addr.timezone_id = tz.id

            self.db.add(addr)
            self.db.flush()

    def replace_for_user(self, user_id: int, items: Iterable[AddressUpdateSchema]) -> None:
        # delete all current addresses
        self.repo.delete_by_user(user_id)
        # recreate
        addresses: list[Address] = []
        for payload in items:
            data = payload.model_dump(exclude_unset=True)
            tz_data = data.get("timezone")

            if tz_data is not None:
                tz = self.tz_service.get_or_create(TimezoneCreateSchema(**tz_data))
                del data["timezone"]

            addr = Address(user_id=user_id, **data)

            if tz_data is not None:
                addr.timezone_id = tz.id

            addresses.append(addr)
        if addresses:
            self.repo.bulk_create(addresses)
