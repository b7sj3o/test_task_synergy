from sqlalchemy import select
from sqlalchemy.orm.session import Session
from app.domain.models.user import User
from app.domain.schemas.user import UserCreate, UserUpdate
from app.exceptions import NotFoundError, ValidationError


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    
    def list(self, skip: int = 0, limit: int = 100, sort: str | None = None) -> list[User]:
        stmt = (
            select(User)
            .offset(skip)
            .limit(limit)
            .order_by(getattr(User, sort))
        )
        result = self.db.execute(stmt)
        return result.scalars().all()


    def get_by_id(self, user_id: int) -> User | None:
        result = self.db.scalar(select(User).where(User.id == user_id))
        return result
    

    def create(self, payload: UserCreate) -> User:
        user = User(**payload.model_dump(exclude={"addresses"}))
        self.db.add(user)
        self.db.flush()
        return user


    def update(self, user_id: int, payload: UserUpdate) -> User | None:
        user = self.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        
        self.db.flush()
        return user


    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        self.db.delete(user)
        self.db.flush()
        return True

