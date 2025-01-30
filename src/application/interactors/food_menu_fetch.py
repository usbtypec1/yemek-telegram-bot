from dataclasses import dataclass

from domain.entities import DailyFoodMenu
from infrastructure.cache import FoodMenuCache
from infrastructure.food_menu import get_food_menu


@dataclass(frozen=True, slots=True, kw_only=True)
class FoodMenuFetchInteractor:
    cache: FoodMenuCache

    async def execute(self) -> list[DailyFoodMenu]:
        daily_food_menu_list = await self.cache.get()
        if daily_food_menu_list is not None:
            return daily_food_menu_list

        daily_food_menu_list = await get_food_menu()
        await self.cache.set(daily_food_menu_list)
        return daily_food_menu_list
