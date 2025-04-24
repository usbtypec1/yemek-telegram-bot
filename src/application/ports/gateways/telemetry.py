from typing import Protocol


class TelemetryGateway(Protocol):
    async def create_usage_record(
        self,
        *,
        user_id: int,
    ) -> None: ...
