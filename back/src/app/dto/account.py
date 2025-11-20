from datetime import datetime
from uuid import UUID

from app.dto.base import BaseDTO


class AccountResponse(BaseDTO):
    id: UUID
    name: str
    current_balance: float
    last_balance_update_at: datetime
