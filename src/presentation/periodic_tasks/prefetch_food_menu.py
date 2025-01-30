from application.interactors.food_menu_fetch import FoodMenuFetchInteractor
from infrastructure.cache import FoodMenuCache


async def prefetch_food_menu(cache: FoodMenuCache):
    await FoodMenuFetchInteractor(cache=cache).execute()
