import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.sqla_persistence.models.base import Base


class Usage(Base):
    __tablename__ = "usages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int]
    user_id: Mapped[int]
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"Usage(id={self.id}, chat_id={self.chat_id}, user_id={self.user_id}, created_at={self.created_at})"
