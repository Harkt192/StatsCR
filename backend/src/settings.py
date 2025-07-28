import secrets
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent

load_dotenv()


class Settings(BaseSettings):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    SECRET_KEY:str = secrets.token_urlsafe(32)
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    SERVER_HOST: str
    APIKEY: str

    @property
    def DATABASE_URL(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                host=self.POSTGRES_HOST,
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                port=5432,
                path=self.POSTGRES_DB
            )
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
