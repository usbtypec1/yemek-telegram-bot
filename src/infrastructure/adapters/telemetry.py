from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.sqla_persistence.models.usage import Usage


@dataclass(frozen=True, slots=True, kw_only=True)
class TelemetryGateway:
    session: AsyncSession

    async def create_usage_record(self, *, user_id: int, chat_id: int) -> None:
        usage = Usage(
            user_id=user_id,
            chat_id=chat_id,
        )
        async with self.session.begin():
            self.session.add(usage)
            await self.session.commit()
