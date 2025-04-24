from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.adapters.food_menu_items import FoodMenuItemGateway


class FoodMenuInfrastructureProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_food_menu_item_gateway(
        self,
        session: AsyncSession,
    ) -> FoodMenuItemGateway:
        return FoodMenuItemGateway(session=session)
