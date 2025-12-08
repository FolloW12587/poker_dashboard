from fastapi import APIRouter

from app.dto.auth import LoginRequest, Token
from presentation.rest.deps import AuthUseCaseDep


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    data: LoginRequest,
    auth_use_case: AuthUseCaseDep,
):
    user = await auth_use_case.authenticate_user(data.username, data.password)

    token = await auth_use_case.create_token_for_user(user)
    return Token(access_token=token)


# @router.post("/register")
async def register(
    data: LoginRequest,
    auth_use_case: AuthUseCaseDep,
):
    user = await auth_use_case.register(data.username, data.password)

    token = await auth_use_case.create_token_for_user(user)
    return Token(access_token=token)
