import datetime
from collections.abc import Iterable
from typing import Protocol

from domain.entities import DailyFoodMenu


class FoodMenuItemGateway(Protocol):
    async def save_food_menu_items(
        self,
        daily_food_menus: Iterable[DailyFoodMenu],
    ) -> None: ...

    async def get_latest_food_menu_items_for_date(
        self,
        date: datetime.date,
    ) -> DailyFoodMenu: ...
