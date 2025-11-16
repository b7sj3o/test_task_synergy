from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = Field(default="Synergy Test API")
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    is_docker: bool = Field(default=False)
    database_url: str = Field(default="postgresql://postgres:postgres@localhost:5432/synergy")
    cors_origins: list[str] = Field(default=["http://localhost:5173", "http://127.0.0.1:5173"])

    @property
    def active_database_url(self) -> str:
        if self.is_docker:
            self.database_url.replace("localhost", "db")
        return self.database_url

settings = Settings()