import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Config:
    telegram_bot_token: str
    food_menu_ttl_in_seconds: int
    redis_url: str


def load_config_from_env() -> Config:
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if telegram_bot_token is None:
        raise ValueError("Telegram bot token missing")

    food_menu_ttl_in_seconds = int(os.getenv("FOOD_MENU_TTL_IN_SECONDS", 900))
    
    redis_url = os.getenv("REDIS_URL", default="redis://127.0.0.1:6379/0")

    return Config(
        telegram_bot_token=telegram_bot_token,
        food_menu_ttl_in_seconds=food_menu_ttl_in_seconds,
        redis_url=redis_url,
    )
