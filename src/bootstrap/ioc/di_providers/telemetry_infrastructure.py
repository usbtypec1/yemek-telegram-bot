from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.adapters.telemetry import TelemetryGateway


class TelemetryInfrastructureProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_telemetry_gateway(
        self,
        session: AsyncSession,
    ) -> TelemetryGateway:
        return TelemetryGateway(session=session)
