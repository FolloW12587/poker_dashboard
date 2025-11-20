import asyncio
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException


class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, timeout: int):
        super().__init__(app)
        self.timeout = timeout

    async def dispatch(self, request, call_next):
        try:
            # Enforce timeout for the request
            return await asyncio.wait_for(call_next(request), timeout=self.timeout)
        except asyncio.TimeoutError as exc:
            # Return a 504 Gateway Timeout response if the request times out
            raise HTTPException(
                status_code=504,
                detail="Request timed out",
            ) from exc
