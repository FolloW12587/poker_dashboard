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
    dsn: str = "sqlite+aiosqlite:///src/infra/db/db.sqlite3"
    use_pgbouncer: bool = False


class ValkeyConfig(BaseModel):
    address: str = "localhost"
    port: int = 6379
    password: str | None = None


class AuthConfig(BaseModel):
    secret: str = "supersecret"


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
