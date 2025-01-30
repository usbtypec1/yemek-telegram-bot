import json
from collections.abc import Iterable
from dataclasses import dataclass

import redis.asyncio as redis


@dataclass(frozen=True, slots=True, kw_only=True)
class FoodMenuCleanerQueue:
    redis_client: redis.Redis

    async def add(self, *, chat_id: int, message_ids: Iterable[int]) -> None:
        await self.redis_client.sadd(
            "food-menu-cleaner-queue",
            json.dumps([chat_id, *message_ids]),
        )

    async def pop_all(self) -> list[tuple[int, tuple[int, ...]]]:
        chat_ids_and_message_ids = await self.redis_client.spop(
            "food-menu-cleaner-queue", 1000,
        )
        result = []
        for chat_id_and_message_ids in chat_ids_and_message_ids:
            chat_id, *message_ids = json.loads(chat_id_and_message_ids)
            result.append((chat_id, message_ids))
        return result
