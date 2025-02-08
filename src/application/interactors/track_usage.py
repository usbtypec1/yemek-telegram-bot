from dataclasses import dataclass

from infrastructure.usage_statistics import UsageStatisticsDao

__all__ = ("TrackUsageInteractor",)


@dataclass(frozen=True, slots=True, kw_only=True)
class TrackUsageInteractor:
    usage_statistics_dao: UsageStatisticsDao

    def execute(self, user_id: int, chat_id: int) -> None:
        self.usage_statistics_dao.add_usage(user_id, chat_id)
