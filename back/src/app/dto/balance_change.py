from datetime import datetime
from enum import Enum
from uuid import UUID

from app.dto.base import BaseDTO


class BalanceChangeState(str, Enum):
    LOCK = "lock"
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    UPDATE = "update"
    SHUTDOWN = "shutdown"


class BalanceChangeResponse(BaseDTO):
    id: UUID
    created_at: datetime

    account_id: UUID
    state: BalanceChangeState
    state_raw: BalanceChangeState
    balance: float
    balance_diff: float


class NewBalanceChangeRequest(BaseDTO):
    account_name: str
    state: BalanceChangeState
    balance: float
