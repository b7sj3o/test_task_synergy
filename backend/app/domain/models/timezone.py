from __future__ import annotations

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils import ReprMixin
from app.infrastructure.db.base import Base


class Timezone(Base, ReprMixin):
    __tablename__ = "timezones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    offset: Mapped[str] = mapped_column(String(16))
    description: Mapped[str] = mapped_column(String(255))

    addresses: Mapped[list["Address"]] = relationship("Address", back_populates="timezone")



