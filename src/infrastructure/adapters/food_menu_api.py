import aiohttp
from pydantic import TypeAdapter

from domain.entities import DailyFoodMenu


def parse_food_menu_response_data(
    response_data: list[dict],
) -> list[DailyFoodMenu]:
    type_adapter = TypeAdapter(list[DailyFoodMenu])
    return type_adapter.validate_python(response_data)


async def get_food_menu_from_api() -> list[DailyFoodMenu]:
    async with aiohttp.ClientSession() as http_client:
        async with http_client.get("https://yemek-api.vercel.app/") as response:
            response_data = await response.json()
            response.raise_for_status()
            return parse_food_menu_response_data(response_data)
