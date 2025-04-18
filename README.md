# Telegram Bot

A simple Telegram bot to check the food menu of [Manas University](https://beslenme.manas.edu.kg/).

Example bot: [@yemek_manas_bot](https://t.me/yemek_manas_bot).

## 📦 Installation

Make sure you have Python 3.8+ installed. Then, clone the repository and install the dependencies:

```bash
uv venv
source .venv/bin/acitvate
uv sync
```


## ⚙️ Configuration
Create a file named config.ini in the root directory with the following content:

```toml
[telegram_bot]
token = "YOUR_BOT_TOKEN"

[access]
chat_id = -100534534234
denied_text = "📲 Для доступа к боту подпишитесь на канал @example"

[cache]
redis_url = "redis://localhost:6379/0"
ttl_in_seconds = 900
```
- token: Your bot's API token from @BotFather.
- chat_id: Allowed Telegram chat ID (e.g. a channel or group).
- denied_text: Message shown to users without access.
- redis_url: Redis server URL for caching.
- ttl_in_seconds: Time to live (in seconds) for cache entries.


## 🚀 Running the Bot
```bash
python src/main.py
```