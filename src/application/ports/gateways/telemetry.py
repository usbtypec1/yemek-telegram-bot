from typing import Protocol


class TelemetryGateway(Protocol):
    async def create_usage_record(
        self,
        *,
        chat_id: int,
        user_id: int,
    ) -> None: ...
