from dataclasses import dataclass
import pathlib
import tomllib
from typing import Final


@dataclass(frozen=True, slots=True)
class Config:
    telegram_bot_token: str
    food_menu_ttl_in_seconds: int
    redis_url: str
    access_chat_id: int
    access_denied_text: str


CONFIG_FILE_PATH: Final[pathlib.Path] = (
    pathlib.Path(__file__).parent.parent / "config.toml"
)


def load_config_from_toml_file(
    config_file_path: pathlib.Path = CONFIG_FILE_PATH,
) -> Config:
    config = tomllib.loads(config_file_path.read_text(encoding="utf-8"))
    return Config(
        telegram_bot_token=config["telegram_bot"]["token"],
        food_menu_ttl_in_seconds=config["cache"]["ttl_in_seconds"],
        redis_url=config["cache"]["redis_url"],
        access_chat_id=config["access"]["chat_id"],
        access_denied_text=config["access"]["denied_text"],
    )
