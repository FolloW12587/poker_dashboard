import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.usecase.errors import (
    ForbiddenError,
    InternalServerError,
    InvalidInputError,
    NotFoundError,
    UnauthorizedError,
)
from infra.utils.config import load_config
from presentation.rest.middleware.timeout import TimeoutMiddleware
from presentation.rest.router.account import router as account_router

cfg = load_config()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(fapp: FastAPI):
    """
    Lifespan function to handle startup and shutdown events.
    """

    yield  # Startup event

    # Останавливаем планировщик при завершении приложения


app = FastAPI(
    title="Poker Dashboard API",
    description="API documentation for the Poker Dashboard application.",
    version="1.0.0",
    docs_url="/swagger",
    lifespan=lifespan,
)

# --- Middleware ---

app.add_middleware(CorrelationIdMiddleware, validator=None)
app.add_middleware(TimeoutMiddleware, timeout=cfg.server.request_timeout)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["OPTIONS", "GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["Content-Range"],
)

# --- Routers ---

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(account_router)

app.include_router(v1_router)


@app.get("/liveness")
def liveness():
    return JSONResponse(
        status_code=200,
        content={"status": "ok"},
    )


@app.get("/readiness")
def readiness():
    return JSONResponse(
        status_code=200,
        content={"status": "ok"},
    )


# --- Exception handlers ---


def error_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"message": message}},
    )


@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "Unhandled exception occurred",
        exc_info=exc,
        extra={
            "error": str(exc),
        },
    )

    return error_response(500, "Internal server error")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return error_response(exc.status_code, exc.detail)


@app.exception_handler(InternalServerError)
def internal_server_error_handler(
    request: Request, exc: InternalServerError
) -> JSONResponse:
    logger.exception(
        "Internal server error occurred",
        exc_info=exc,
        extra={
            "error": str(exc),
        },
    )

    return error_response(500, "Internal server error")


@app.exception_handler(NotFoundError)
def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return error_response(404, exc.message)


@app.exception_handler(InvalidInputError)
def invalid_input_handler(request: Request, exc: InvalidInputError) -> JSONResponse:
    return error_response(400, exc.message)


@app.exception_handler(UnauthorizedError)
def unauthorized_handler(request: Request, exc: UnauthorizedError) -> JSONResponse:
    return error_response(401, exc.message)


@app.exception_handler(ForbiddenError)
def forbidden_handler(request: Request, exc: ForbiddenError) -> JSONResponse:
    return error_response(403, exc.message)
