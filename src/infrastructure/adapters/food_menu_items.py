from collections.abc import Iterable
import datetime
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.entities import DailyFoodMenu, FoodMenuItem
from infrastructure.sqla_persistence.models.food_menu_item import (
    FoodMenuItem as FoodMenuItemModel,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class FoodMenuItemGateway:
    session: AsyncSession

    async def save_food_menu_items(
        self,
        daily_food_menus: Iterable[DailyFoodMenu],
    ) -> None:
        async with self.session.begin():
            items_to_update: list[FoodMenuItemModel] = []
            items_to_add: list[FoodMenuItemModel] = []
            for new_daily_food_menu in daily_food_menus:
                old_daily_food_menu = (
                    await self.get_latest_food_menu_items_for_date(
                        date=new_daily_food_menu.at,
                    )
                )
                old_item_name_to_item = {
                    item.name: item for item in old_daily_food_menu.items
                }
                new_item_name_to_item = {
                    item.name: item for item in new_daily_food_menu.items
                }

                inactive_item_names = set(old_item_name_to_item) - set(
                    new_item_name_to_item
                )
                new_item_names = set(new_item_name_to_item) - set(
                    old_item_name_to_item
                )
                for inactive_item_name in inactive_item_names:
                    item = old_item_name_to_item[inactive_item_name]
                    items_to_update.append(
                        FoodMenuItemModel(
                            name=item.name,
                            calories_count=item.calories_count,
                            photo_url=item.photo_url,
                            date=new_daily_food_menu.at,
                            is_active=False,
                        )
                    )

                for new_item_name in new_item_names:
                    item = new_item_name_to_item[new_item_name]
                    items_to_add.append(
                        FoodMenuItemModel(
                            name=item.name,
                            calories_count=item.calories_count,
                            photo_url=item.photo_url,
                            date=new_daily_food_menu.at,
                        )
                    )

            if items_to_add:
                self.session.add_all(items_to_add)
            if items_to_update:
                for item in items_to_update:
                    await self.session.merge(item)
            await self.session.commit()

    async def get_latest_food_menu_items_for_date(
        self, date: datetime.date
    ) -> DailyFoodMenu:
        statement = select(FoodMenuItemModel).where(
            FoodMenuItemModel.date == date,
            FoodMenuItemModel.is_active,
        )
        food_menu_items = await self.session.scalars(statement)
        await self.session.commit()
        
        items: list[FoodMenuItem] = []
        for food_menu_item in food_menu_items:
            items.append(
                FoodMenuItem(
                    name=food_menu_item.name,
                    calories_count=food_menu_item.calories_count,
                    photo_url=food_menu_item.photo_url,
                )
            )
        return DailyFoodMenu(
            at=date,
            items=items,
        )
