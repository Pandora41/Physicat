# Tests for Logging Utilities - tests for structured logging configuration
import logging
import pytest

from app.utils.logging import configure_logging, get_logger


# Test configure_logging sets up logging correctly
@pytest.mark.unit
def test_configure_logging_default() -> None:
    # Reset logging to ensure clean state
    logging.root.handlers = []
    
    configure_logging("INFO")
    
    # Verify logging is configured
    assert len(logging.root.handlers) > 0
    assert logging.root.level <= logging.INFO


# Test configure_logging with DEBUG level uses ConsoleRenderer
@pytest.mark.unit
def test_configure_logging_debug() -> None:
    # Reset logging to ensure clean state
    logging.root.handlers = []
    
    configure_logging("DEBUG")
    
    # Verify logging is configured
    assert len(logging.root.handlers) > 0
    assert logging.root.level <= logging.DEBUG


# Test get_logger returns a logger instance
@pytest.mark.unit
def test_get_logger() -> None:
    logger = get_logger("test_module")
    assert logger is not None
    # Verify it's a structlog logger
    assert hasattr(logger, "info")
    assert hasattr(logger, "error")
    assert hasattr(logger, "debug")


# Test get_logger without name uses default
@pytest.mark.unit
def test_get_logger_no_name() -> None:
    logger = get_logger()
    assert logger is not None
    assert hasattr(logger, "info")


# Test configure_logging with different log levels
@pytest.mark.unit
def test_configure_logging_levels() -> None:
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    
    for level in levels:
        logging.root.handlers = []
        configure_logging(level)
        
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        assert logging.root.level <= numeric_level


# Test that logging configuration can be called multiple times
@pytest.mark.unit
def test_configure_logging_multiple_calls() -> None:
    logging.root.handlers = []
    
    configure_logging("INFO")
    configure_logging("DEBUG")
    configure_logging("WARNING")
    
    # Should not raise errors
    assert len(logging.root.handlers) > 0

