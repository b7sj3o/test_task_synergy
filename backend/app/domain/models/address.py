from __future__ import annotations
from datetime import datetime

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils import ReprMixin
from app.infrastructure.db.base import Base


class Address(Base, ReprMixin):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    street: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100))
    postcode: Mapped[str] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="addresses")

    timezone_id: Mapped[int | None] = mapped_column(ForeignKey("timezones.id"), nullable=True)
    timezone: Mapped["Timezone"] = relationship("Timezone", back_populates="addresses")
