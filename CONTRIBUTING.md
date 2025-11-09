# Contributing Guide

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Schrodicats
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run environment validation**
   ```bash
   python scripts/test_env.py
   ```

## Code Style

- Use **type hints** everywhere
- Follow **Google-style docstrings**
- Use **black** for code formatting
- Maximum line length: **88 characters** (black default)

## Testing

- Write tests for all new features
- Maintain **>95% code coverage**
- Run tests before committing:
  ```bash
  pytest -q --cov=app --cov-report=term-missing
  ```

## Git Workflow

1. Create a feature branch
2. Make your changes
3. Run tests and ensure they pass
4. Commit with descriptive messages
5. Push and create a pull request

## Project Structure

```
app/
  routes/     # API blueprints
  models/     # Database models
  utils/      # Utilities and helpers
tests/        # Test suite
scripts/      # Utility scripts
```

## Type Hints

Always use type hints:

```python
def my_function(param: str) -> dict[str, Any]:
    """Function description."""
    return {"key": "value"}
```

## Documentation

- All functions must have Google-style docstrings
- Include type information in docstrings
- Document complex logic and algorithms



