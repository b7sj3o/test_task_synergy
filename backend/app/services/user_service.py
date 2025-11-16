from __future__ import annotations

from sqlalchemy.orm import Session

from app.services.address_service import AddressService
from app.domain.models import User
from app.domain.schemas import UserCreate, UserUpdate
from app.exceptions import ValidationError, NotFoundError
from app.infrastructure.db.repositories import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)
        self.address_service = AddressService(db)

    def list_users(self, skip: int = 0, limit: int = 100, sort: str | None = None) -> list[User]:
        if sort and sort not in {"first_name", "last_name", "email"}:
            raise ValidationError("Invalid sort field")
        return self.repo.list(skip=skip, limit=limit, sort=sort or "id")

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.repo.get_by_id(user_id)

    def create_user(self, payload: UserCreate) -> User:
        user = self.repo.create(payload)
        if payload.addresses:
            self.address_service.attach_to_user(user.id, payload.addresses)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id: int, payload: UserUpdate) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        scalar_payload = payload.model_dump(exclude_unset=True, exclude={"addresses"})
        if scalar_payload:
            self.repo.update(user_id, UserUpdate(**scalar_payload))

        if payload.addresses is not None:
            self.address_service.replace_for_user(user_id, payload.addresses)

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        ok = self.repo.delete(user_id)
        self.db.commit()
        return ok





