import base64
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import os
from typing import Optional
from uuid import UUID
from jose import jwt

from app.dto.auth import TokenUser
from app.usecase.errors import InvalidInputError, UnauthorizedError
from domain.entity.user import User
from infra.db.user import UserRepository
from infra.utils.config import AuthConfig


class AuthUseCase:

    def __init__(self, cfg: AuthConfig, user_repo: UserRepository) -> None:
        self._cfg = cfg
        self.user_repo = user_repo

    async def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> User:
        user = await self.user_repo.get_by_name(username)

        if not user or not self._verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid password")

        # update last login
        user.last_login = datetime.now(timezone.utc)
        user = await self.user_repo.update(user)

        return user

    async def register(self, username: str, password: str) -> User:
        if await self.user_repo.get_by_name(username):
            raise InvalidInputError("User with given username already exists")

        if len(password) < 8:
            raise InvalidInputError("Password is to short")

        user = User(
            username=username,
            last_login=datetime.now(timezone.utc),
            password_hash=self._hash_password(password),
        )

        return await self.user_repo.create(user)

    async def create_token_for_user(self, user: User) -> str:
        return self._create_access_token({"sub": str(user.id)})

    def get_user_from_token(self, token: str) -> TokenUser:
        try:
            payload = jwt.decode(
                token, self._cfg.secret, algorithms=[self._cfg.algorithm]
            )
            user_id = UUID(payload.get("sub"))
        except Exception:
            raise UnauthorizedError("Invalid token")

        return TokenUser(id=user_id)

    def _hash_password(self, password: str) -> str:
        """
        Returns base64(salt + pbkdf2_hash).
        """
        salt = os.urandom(16)
        hash_bytes = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            200_000,  # OWASP recommended
        )
        return base64.b64encode(salt + hash_bytes).decode()

    def _verify_password(self, password: str, stored_hash: str) -> bool:
        decoded = base64.b64decode(stored_hash.encode())

        salt = decoded[:16]
        stored_bytes = decoded[16:]

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            200_000,
        )

        return hmac.compare_digest(stored_bytes, new_hash)

    def _create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=self._cfg.access_token_expires_minutes)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self._cfg.secret, algorithm=self._cfg.algorithm)
