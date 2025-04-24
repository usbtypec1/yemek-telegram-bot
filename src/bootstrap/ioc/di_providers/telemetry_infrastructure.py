from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class TelemetryInfrastructureProvider(Provider):
    
    @provide(scope=Scope.REQUEST)
    def provide_async_session_maker(self) -> async_sessionmaker[AsyncSession]:
        pass
        
    @provide(scope=Scope.REQUEST)
    def provide_async_session(self) -> AsyncSession:
        pass