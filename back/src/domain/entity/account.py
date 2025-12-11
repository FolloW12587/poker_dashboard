from datetime import datetime
from sqlalchemy import DateTime, text
from sqlalchemy.orm import Mapped, mapped_column

from domain.entity.base import BaseEntity


class Account(BaseEntity):
    __tablename__ = "accounts"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    balance: Mapped[float]
    is_balance_fixed: Mapped[bool] = mapped_column(
        default=False, server_default=text("false")
    )
    last_balance_update: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))
