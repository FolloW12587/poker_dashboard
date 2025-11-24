from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from domain.entity.base import BaseEntity


class User(BaseEntity):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    password_hash: Mapped[str]
