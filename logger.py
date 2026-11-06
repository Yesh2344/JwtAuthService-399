import logging
import sys
from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": sys.stdout,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

def configure_logging() -> None:
    """Apply the logging configuration."""
    dictConfig(LOGGING_CONFIG)

configure_logging()
logger = logging.getLogger(__name__)