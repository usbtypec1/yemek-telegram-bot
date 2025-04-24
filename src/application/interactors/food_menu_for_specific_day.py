from dataclasses import dataclass

from application.ports.gateways.food_menu_items import FoodMenuItemGateway
from domain.entities import DailyFoodMenu
from domain.services.food_menu import get_date_after_skip


@dataclass(frozen=True, slots=True, kw_only=True)
class FoodMenuForSpecificDayPickInteractor:
    food_menu_item_gateway: FoodMenuItemGateway
    days_to_skip: int

    async def execute(self) -> DailyFoodMenu:
        date = get_date_after_skip(self.days_to_skip)
        return await self.food_menu_item_gateway.get_latest_food_menu_items_for_date(
            date=date,
        )
