import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.sqla_persistence.models.base import Base


class FoodMenuItem(Base):
    __tablename__ = "food_menu_items"

    name: Mapped[str] = mapped_column(primary_key=True)
    calories_count: Mapped[int]
    photo_url: Mapped[str]
    date: Mapped[datetime.date] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    def __repr__(self) -> str:
        return f"FoodMenuItem(name={self.name}, price={self.calories_count}, photo_url={self.photo_url}, date={self.date})"
