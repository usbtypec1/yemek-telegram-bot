import datetime
from zoneinfo import ZoneInfo


def get_date_after_skip(days_to_skip: int) -> datetime.date:
    timezone = ZoneInfo("Asia/Bishkek")
    now = datetime.datetime.now(timezone)
    return (now + datetime.timedelta(days=days_to_skip)).date()
