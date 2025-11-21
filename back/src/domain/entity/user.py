from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from domain.entity.base import BaseEntity


class User(BaseEntity):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    last_login: Mapped[datetime]
    password_hash: Mapped[str]
