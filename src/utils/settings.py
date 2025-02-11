from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
from loguru import logger

class _PostgresSettings(BaseSettings):
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "postgr"
    postgres_port: int = 5432
    postgres_db: str = "postgres"

    # Свойство для формирования DSN (Data Source Name)
    @property
    def dsn(self) -> str:
        instance = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db,
        )  # pyright: ignore[reportUnknownVariableType]
        url_str = instance.unicode_string()

        logger.info(f'Ссылка на БД создана: {url_str}')

        return url_str

    class Config:
        env_prefix: str = "POSTGRES_"
        case_sensitive: bool = False


class Settings(BaseSettings):
    postgres: _PostgresSettings = _PostgresSettings()


settings = Settings()
