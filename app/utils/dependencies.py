# Dependency Injection Utilities - provides dependency injection patterns for Flask routes
from typing import Any, Callable, TypeVar, ParamSpec

from flask import current_app

P = ParamSpec("P")
T = TypeVar("T")


# Get database session dependency (can be extended to use dependency injection frameworks)
def get_db() -> Any:
    from app import db
    return db


# Get application settings dependency
def get_settings() -> Any:
    from app.config import get_settings as _get_settings
    return _get_settings()


# Decorator for injecting dependencies into route handlers (simple DI pattern, can be extended)
def inject_dependencies(**deps: Callable) -> Callable:
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            # Inject dependencies
            for dep_name, dep_factory in deps.items():
                if dep_name not in kwargs:
                    kwargs[dep_name] = dep_factory()
            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    return decorator

