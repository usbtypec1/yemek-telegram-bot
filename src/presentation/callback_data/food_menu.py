from aiogram.filters.callback_data import CallbackData


class FoodMenuCallbackData(CallbackData, prefix="food-menu"):
    days_to_skip: int
