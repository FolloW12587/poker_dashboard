from enum import Enum
from uuid import UUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from domain.entity.base import BaseEntity


class BalanceChangeState(str, Enum):
    LOCK = "lock"
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    UPDATE = "update"


class BalanceChange(BaseEntity):
    __tablename__ = "balance_changes"

    account_id: Mapped[UUID]
    state_raw: Mapped[BalanceChangeState] = mapped_column(String)
    state: Mapped[BalanceChangeState] = mapped_column(String)
    balance: Mapped[float]
    balance_diff: Mapped[float]
