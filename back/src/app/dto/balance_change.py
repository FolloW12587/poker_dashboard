from datetime import datetime
from enum import Enum
from uuid import UUID

from app.dto.base import BaseDTO


class BalanceStateChange(str, Enum):
    MONEY_REQUEST = "money_request"
    MONEY_RECIEVED = "money_received"
    MONEY_WITHDRAW = "money_withdraw"
    UPDATE = "update"


class BalanceChangeResponse(BaseDTO):
    id: UUID
    created_at: datetime

    account_id: UUID
    state: BalanceStateChange
    balance: float


class BalanceChangeRequest(BaseDTO):
    account_name: str
    state: BalanceStateChange
    balance: float
