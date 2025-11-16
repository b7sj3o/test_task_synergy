from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

engine = create_engine(settings.active_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



