from dataclasses import dataclass

from pydantic import TypeAdapter, ValidationError
import redis.asyncio as redis

from domain.entities import DailyFoodMenu


@dataclass(frozen=True, slots=True, kw_only=True)
class FoodMenuCache:
    redis_client: redis.Redis
    ttl_in_seconds: int
    
    type_adapter = TypeAdapter(list[DailyFoodMenu])

    async def get(self) -> list[DailyFoodMenu] | None:
        food_menu_json = await self.redis_client.get("food_menu")

        if food_menu_json is None:
            return

        try:
            return self.type_adapter.validate_json(food_menu_json)
        except ValidationError:
            return

    async def set(self, food_menu: list[DailyFoodMenu]) -> None:
        await self.redis_client.set(
            "food_menu", self.type_adapter.dump_json(food_menu)
        )
        await self.redis_client.expire("food_menu", self.ttl_in_seconds)
