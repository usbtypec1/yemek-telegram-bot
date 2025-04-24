from dataclasses import dataclass

from application.ports.gateways.telemetry import TelemetryGateway


@dataclass(frozen=True, slots=True, kw_only=True)
class TrackUsageInteractor:
    telemetry_gateway: TelemetryGateway
    user_id: int
    chat_id: int

    async def execute(self) -> None:
        await self.telemetry_gateway.create_usage_record(
            user_id=self.user_id,
            chat_id=self.chat_id,
        )
