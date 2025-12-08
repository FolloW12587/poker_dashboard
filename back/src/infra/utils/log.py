import logging
import logging.config

from infra.utils.config import LogConfig, LogType, load_config

CORRELATION_ID_FILTER = {
    "correlation_id": {
        "()": "asgi_correlation_id.CorrelationIdFilter",
        "uuid_length": 32,
        "default_value": "-",
    },
}

JSON_FMT = (
    "%(asctime)s %(levelname)s %(correlation_id)s"
    + "%(name)s %(message)s %(filename)s:%(lineno)d"
)
CONSOLE_FMT = (
    "%(asctime)s %(levelname)s [%(correlation_id)s] "
    + "%(name)s %(message)s (%(filename)s:%(lineno)d)"
)


def setup_logging(cfg: LogConfig) -> None:
    """Setup unified logging configuration for all loggers in the project."""

    # Base formatter configuration
    formatters = {}
    if cfg.type == LogType.JSON:
        formatters = {
            "json": {
                "()": "pythonjsonlogger.json.JsonFormatter",
                "fmt": JSON_FMT,
                "rename_fields": {"levelname": "level"},
            }
        }
        default_formatter = "json"
    elif cfg.type == LogType.CONSOLE:  # CONSOLE
        formatters = {
            "console": {
                "format": CONSOLE_FMT,
            }
        }
        default_formatter = "console"
    else:  # FILE
        formatters = {
            "file": {
                "format": CONSOLE_FMT,
            }
        }
        default_formatter = "file"

    handlers = {
        "default": {
            "formatter": default_formatter,
            "class": "logging.StreamHandler",
            "filters": ["correlation_id"],
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": default_formatter,
            "class": "logging.StreamHandler",
            "filters": ["correlation_id"],
            "stream": "ext://sys.stdout",
        },
    }
    if cfg.type == LogType.FILE:
        handlers = {
            "default": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "logs/app.log",
                "maxBytes": 10_000_000,
                "backupCount": 5,
                "formatter": default_formatter,
                "filters": ["correlation_id"],
            },
            "access": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "logs/access.log",
                "maxBytes": 10_000_000,
                "backupCount": 5,
                "formatter": default_formatter,
                "filters": ["correlation_id"],
            },
        }

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {**CORRELATION_ID_FILTER},
        "formatters": formatters,
        "handlers": handlers,
        "loggers": {
            # Application logger
            cfg.name: {
                "handlers": ["default"],
                "level": cfg.level,
                "propagate": False,
            },
            # Uvicorn loggers
            "uvicorn": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["access"],
                "level": "INFO",
                "propagate": False,
            },
            # SQLAlchemy loggers
            "sqlalchemy.engine": {
                "handlers": ["default"],
                "level": "WARNING",
                "propagate": False,
            },
            "sqlalchemy.engine.Engine": {
                "handlers": ["default"],
                "level": "WARNING",
                "propagate": False,
            },
            "sqlalchemy.dialects": {
                "handlers": ["default"],
                "level": "WARNING",
                "propagate": False,
            },
            "sqlalchemy.pool": {
                "handlers": ["default"],
                "level": "WARNING",
                "propagate": False,
            },
            "sqlalchemy.orm": {
                "handlers": ["default"],
                "level": "WARNING",
                "propagate": False,
            },
            # Root logger fallback
            "": {
                "handlers": ["default"],
                "level": "INFO",
            },
        },
        "root": {
            "handlers": ["default"],
            "level": "INFO",
        },
    }

    logging.config.dictConfig(log_config)


def get_uvicorn_log_config() -> dict:
    """Get uvicorn-compatible logging configuration."""
    cfg = load_config()

    # Setup the main logging first
    setup_logging(cfg.log)

    # Return minimal config since we've already configured everything
    return {
        "version": 1,
        "disable_existing_loggers": False,
    }


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the project's configuration."""
    return logging.getLogger(name)


# Initialize logging on module import
setup_logging(load_config().log)

# Default logger for the application
logger = get_logger(load_config().log.name)
