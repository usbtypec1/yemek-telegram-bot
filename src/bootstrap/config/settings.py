import pathlib
import tomllib
from typing import Final, Self

from pydantic import BaseModel, PostgresDsn


ROOT_PATH: Final[pathlib.Path] = pathlib.Path(
    __file__
).parent.parent.parent.parent
SETTINGS_FILE_PATH: Final[pathlib.Path] = ROOT_PATH / "config.toml"


class DatabaseSettings(BaseModel):
    host: str
    port: int
    user: str
    password: str
    name: str

    @property
    def dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.name,
            )
        )


class TelegramBotSettings(BaseModel):
    token: str


class AccessSettings(BaseModel):
    chat_id: int
    denied_text: str


class Settings(BaseModel):
    telegram_bot: TelegramBotSettings
    access: AccessSettings
    database: DatabaseSettings

    @classmethod
    def from_toml(cls) -> Self:
        settings_toml = SETTINGS_FILE_PATH.read_text(encoding="utf-8")
        settings = tomllib.loads(settings_toml)
        return cls.model_validate(settings)
