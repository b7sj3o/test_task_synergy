from __future__ import annotations
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine
from app.api.routes.users import router as users_router
from app.api.routes.random import router as random_router


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        Base.metadata.create_all(bind=engine)
        yield

    application = FastAPI(title="Synergy Test API", debug=settings.debug, lifespan=lifespan)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(users_router)
    application.include_router(random_router)

    return application


app = create_app()
