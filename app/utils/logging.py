# Structured Logging Configuration - configures structlog for structured, JSON-formatted logging
import logging
import sys
from typing import Any

import structlog
from structlog.types import Processor


# Configure structured logging with structlog - sets up processors for timestamp, log level, JSON/console rendering
def configure_logging(log_level: str = "INFO") -> None:
    # Convert string level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=numeric_level,
    )

    # Configure structlog processors
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
    ]

    # Add timestamp processor
    processors.insert(0, structlog.processors.TimeStamper(fmt="iso"))

    # Add JSON renderer for production, console for development
    if log_level.upper() == "DEBUG":
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        processors.append(structlog.processors.JSONRenderer())

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(numeric_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


# Get a configured structlog logger instance (optional logger name, uses calling module name if None)
def get_logger(name: str | None = None) -> structlog.BoundLogger:
    return structlog.get_logger(name)

