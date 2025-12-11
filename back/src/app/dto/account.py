from datetime import datetime
from uuid import UUID

from app.dto.base import BaseDTO


class AccountResponse(BaseDTO):
    id: UUID
    name: str
    balance: float
    last_balance_update: datetime
    is_balance_fixed: bool
    is_active: bool
