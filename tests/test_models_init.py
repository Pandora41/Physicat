# Tests for Models Init - tests for models module initialization
import pytest


# Test that BaseModel can be imported from models module
@pytest.mark.unit
def test_models_init_import() -> None:
    from app.models import BaseModel
    
    assert BaseModel is not None
    assert hasattr(BaseModel, "__abstract__")
    assert BaseModel.__abstract__ is True

