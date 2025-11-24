import os
from enum import Enum
from functools import lru_cache

import yaml
from pydantic import BaseModel

CONFIG_PATH = "./config/config.yml"


class LogType(str, Enum):
    JSON = "json"
    CONSOLE = "console"


class LogConfig(BaseModel):
    name: str = "app"
    level: str = "INFO"
    type: LogType = LogType.CONSOLE


class ServerConfig(BaseModel):
    request_timeout: int = 60  # in seconds


class DatabaseConfig(BaseModel):
    dsn: str = "sqlite+aiosqlite:///infra/db/db.sqlite3"
    use_pgbouncer: bool = False


class ValkeyConfig(BaseModel):
    address: str = "localhost"
    port: int = 6379
    password: str | None = None


class AuthConfig(BaseModel):
    secret: str = "supersecret"
    algorithm: str = "HS256"
    access_token_expires_minutes: int = 60

    api_secret: str = (
        "XahagS9FOnMopwVQN0wI7M8e1vLH+EFRRXg3l3iDGjI12whe4ckO8rb/jB43XgGw"  # apisecret
    )


class Config(BaseModel):
    env: str = "local"
    log: LogConfig = LogConfig()
    server: ServerConfig = ServerConfig()
    db: DatabaseConfig = DatabaseConfig()
    valkey: ValkeyConfig = ValkeyConfig()
    auth: AuthConfig = AuthConfig()


@lru_cache(maxsize=1)
def load_config() -> Config:
    if not os.path.exists(CONFIG_PATH):
        print(f"Config file not found at {CONFIG_PATH}. Using default config.")

        return Config()

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config_data = yaml.safe_load(file)

    print(f"Config loaded from {CONFIG_PATH}")

    return Config(**config_data)
