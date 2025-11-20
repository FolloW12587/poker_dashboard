from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from domain.entity.base import BaseEntity


class Account(BaseEntity):
    __tablename__ = "accounts"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    current_balance: Mapped[float]
    last_balance_update: Mapped[datetime]
