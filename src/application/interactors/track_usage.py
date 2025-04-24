from dataclasses import dataclass

from application.ports.gateways.telemetry import TelemetryGateway


@dataclass(frozen=True, slots=True, kw_only=True)
class TrackUsageInteractor:
    telemetry_gateway: TelemetryGateway

    async def execute(self, *, user_id: int, chat_id: int) -> None:
        await self.telemetry_gateway.create_usage_record(
            user_id=user_id,
            chat_id=chat_id,
        )
