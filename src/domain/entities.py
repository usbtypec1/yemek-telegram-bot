import datetime

from pydantic import BaseModel


class FoodMenuItem(BaseModel):
    name: str
    calories_count: int
    photo_url: str


class DailyFoodMenu(BaseModel):
    items: list[FoodMenuItem]
    at: datetime.date
