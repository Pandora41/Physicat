# Project Structure Documentation

## Overview

This is a production-ready Flask 3.x RESTful API project with Python 3.11, following modern best practices and 2025 standards.

## Directory Structure

```
Schrodicats/
├── app/                          # Main application package
│   ├── __init__.py              # Flask app factory with blueprints
│   ├── config.py                # Pydantic v2 settings management
│   ├── routes/                  # API route blueprints
│   │   ├── __init__.py
│   │   ├── health.py            # Health check endpoints
│   │   └── api_v1.py            # Main API v1 endpoints
│   ├── models/                   # SQLAlchemy database models
│   │   ├── __init__.py
│   │   └── base.py              # Base model with common fields
│   └── utils/                    # Utility modules
│       ├── __init__.py
│       ├── logging.py            # Structured logging setup
│       └── dependencies.py       # Dependency injection utilities
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures and configuration
│   ├── test_health.py            # Health endpoint tests
│   ├── test_api_v1.py            # API v1 endpoint tests
│   └── test_config.py            # Configuration tests
│
├── scripts/                      # Utility scripts
│   ├── test_env.py              # Environment validation & test runner
│   └── run.py                    # Production server runner
│
├── .gitignore                    # Git ignore patterns
├── .dockerignore                 # Docker ignore patterns
├── requirements.txt              # Pinned Python dependencies
├── pytest.ini                    # Pytest configuration
├── Dockerfile                    # Multi-stage production Dockerfile
├── docker-compose.yml            # Local development with PostgreSQL
├── Makefile                      # Convenience commands
├── setup.py                      # Package setup (optional)
├── env.example                   # Environment variables template
├── README.md                     # Main documentation
├── CONTRIBUTING.md               # Contribution guidelines
└── PROJECT_STRUCTURE.md          # This file
```

## Key Features

### 1. Application Factory Pattern
- `app/__init__.py` uses factory pattern for testability
- Supports dependency injection
- Configurable via Pydantic settings

### 2. Configuration Management
- `app/config.py` uses Pydantic v2 for type-safe settings
- Environment variable support
- LRU cache for performance

### 3. Structured Logging
- `app/utils/logging.py` configures structlog
- JSON formatting for production
- Console formatting for development

### 4. API Documentation
- Auto-generated OpenAPI/Swagger docs via Flasgger
- Accessible at `/apidocs`
- Integrated with route docstrings

### 5. Testing
- Comprehensive test suite with >95% coverage requirement
- Pytest with fixtures in `conftest.py`
- Test database isolation

### 6. Environment Validation
- `scripts/test_env.py` ensures:
  - Virtual environment is active
  - Python version is 3.11.9
  - Requirements are up-to-date (hash-based)
  - Tests pass with >95% coverage
  - Server starts only if all checks pass

### 7. Docker Support
- Multi-stage Dockerfile (<100MB final image)
- docker-compose.yml with PostgreSQL
- Health checks configured
- Non-root user for security

## Technology Stack

- **Runtime**: Python 3.11.9
- **Framework**: Flask 3.0.3
- **Database**: SQLAlchemy 2.0.35, PostgreSQL support
- **Validation**: Pydantic 2.9.2
- **Logging**: structlog 24.2.0
- **Documentation**: Flasgger 0.9.7.1
- **Testing**: pytest 8.3.3, pytest-cov 5.0.0
- **Server**: Gunicorn 23.0.0

## Best Practices Implemented

1. ✅ Type hints everywhere
2. ✅ Google-style docstrings
3. ✅ Dependency injection patterns
4. ✅ Application factory pattern
5. ✅ Blueprint architecture
6. ✅ Structured logging
7. ✅ Comprehensive testing
8. ✅ Environment validation
9. ✅ Docker multi-stage builds
10. ✅ Security best practices (non-root user, secrets management)

## Next Steps

To extend this project:

1. Add more models in `app/models/`
2. Create new blueprints in `app/routes/`
3. Add utilities in `app/utils/`
4. Write tests in `tests/`
5. Update `requirements.txt` as needed



