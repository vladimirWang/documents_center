import os
from functools import lru_cache
from pathlib import Path


def _load_dotenv() -> None:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.database_url = os.getenv(
            "SQLALCHEMY_DATABASE_URL",
            "postgresql+psycopg://postgres@127.0.0.1:5432/documents_center",
        )

    @property
    def async_database_url(self) -> str:
        if self.database_url.startswith("postgresql+psycopg://"):
            return self.database_url.replace(
                "postgresql+psycopg://",
                "postgresql+psycopg_async://",
                1,
            )
        return self.database_url


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
