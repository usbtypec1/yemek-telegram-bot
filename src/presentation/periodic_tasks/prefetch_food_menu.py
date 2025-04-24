from dishka import AsyncContainer

from application.interactors.food_menu_fetch import (
    FoodMenuFetchAndSaveInteractor,
)
from infrastructure.adapters.food_menu_items import FoodMenuItemGateway


async def prefetch_food_menu(
    container: AsyncContainer,
):
    async with container() as request_container:
        food_menu_item_gateway = await request_container.get(
            FoodMenuItemGateway,
        )
        await FoodMenuFetchAndSaveInteractor(
            food_menu_item_gateway=food_menu_item_gateway,
        ).execute()
