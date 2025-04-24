import logging
from dataclasses import dataclass

from application.ports.gateways.food_menu_items import FoodMenuItemGateway
from infrastructure.adapters.food_menu_api import get_food_menu_from_api


log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class FoodMenuFetchAndSaveInteractor:
    food_menu_item_gateway: FoodMenuItemGateway

    async def execute(self) -> None:
        daily_food_menu_items = await get_food_menu_from_api()
        log.info("Fetched food menu items from API")
        await self.food_menu_item_gateway.save_food_menu_items(
            daily_food_menu_items,
        )
        log.info("Saved food menu items to database")
