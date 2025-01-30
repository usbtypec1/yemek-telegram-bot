import datetime
from zoneinfo import ZoneInfo
from collections.abc import Sequence

from domain.entities import DailyFoodMenu


def pick_for_specific_day(
    *,
    daily_food_menu_list: Sequence[DailyFoodMenu],
    days_to_skip: int,
) -> DailyFoodMenu | None:
    timezone = ZoneInfo("Asia/Bishkek")
    now = datetime.datetime.now(timezone)

    date_to_pick = (now + datetime.timedelta(days=days_to_skip)).date()

    for daily_food_menu in daily_food_menu_list:
        if daily_food_menu.at == date_to_pick:
            return daily_food_menu
