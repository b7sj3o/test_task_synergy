from __future__ import annotations

from typing import Iterable
from sqlalchemy import select, delete
from sqlalchemy.orm.session import Session

from app.domain.models import Address


class AddressRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_user(self, user_id: int) -> list[Address]:
        return self.db.execute(select(Address).where(Address.user_id == user_id)).scalars().all()

    def delete_by_user(self, user_id: int) -> None:
        self.db.execute(delete(Address).where(Address.user_id == user_id))

    def create(self, address: Address) -> Address:
        self.db.add(address)
        self.db.flush()
        return address

    def bulk_create(self, addresses: Iterable[Address]) -> None:
        self.db.add_all(list(addresses))
        self.db.flush()
