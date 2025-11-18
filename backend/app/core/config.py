
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str
    debug: bool
    is_docker: bool
    database_url: str
    cors_origins: list[str]

    @property
    def active_database_url(self) -> str:
        if self.is_docker:
            self.database_url = self.database_url.replace("localhost", "db")
        return self.database_url


settings = Settings()
