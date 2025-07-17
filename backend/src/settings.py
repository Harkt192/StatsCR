import secrets
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY:str = secrets.token_urlsafe(32)
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    SERVER_HOST: str
    API_TOKEN: str

    @property
    def DATABASE_URL(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                host=self.POSTGRES_HOST,
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                port=5432

            )
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
