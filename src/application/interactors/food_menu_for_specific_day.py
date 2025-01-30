from dataclasses import dataclass

from domain.entities import DailyFoodMenu
from domain.services.food_menu import pick_for_specific_day


@dataclass(frozen=True, slots=True, kw_only=True)
class FoodMenuForSpecificDayPickInteractor:
    daily_food_menu_list: list[DailyFoodMenu]
    days_to_skip: int

    def execute(self) -> DailyFoodMenu | None:
        return pick_for_specific_day(
            daily_food_menu_list=self.daily_food_menu_list,
            days_to_skip=self.days_to_skip,
        )
