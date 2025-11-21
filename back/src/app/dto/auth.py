from uuid import UUID

from pydantic import BaseModel


class TokenUser(BaseModel):
    id: UUID


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str
