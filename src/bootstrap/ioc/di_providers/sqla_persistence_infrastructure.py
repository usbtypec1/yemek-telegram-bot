from collections.abc import AsyncGenerator
from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from infrastructure.sqla_persistence.models.base import Base
from bootstrap.config.settings import Settings


class SQLAlchemyPersistenceInfrastructureProvider(Provider):
    settings = from_context(Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def provide_async_engine(
        self, settings: Settings
    ) -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(settings.database.dsn)

        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        yield engine
        await engine.dispose()

    @provide(scope=Scope.REQUEST)
    def provide_async_session_maker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autoflush=False,
        )

    @provide(scope=Scope.REQUEST)
    async def provide_async_session(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session
