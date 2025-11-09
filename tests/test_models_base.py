# Tests for Base Model - tests for the BaseModel class with common fields and methods
import pytest
from datetime import datetime

from app import db
from app.models.base import BaseModel


# Create a test model that inherits from BaseModel
# Note: Using SampleModel instead of TestModel to avoid pytest collection
class SampleModel(BaseModel):
    __tablename__ = "sample_models"
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer, default=0)


# Test that BaseModel has required fields (id, created_at, updated_at)
def test_base_model_fields(app, reset_db) -> None:
    with app.app_context():
        db.create_all()
        
        # Create a test instance
        test_instance = SampleModel(name="test", value=42)
        db.session.add(test_instance)
        db.session.commit()
        
        # Check that all base fields exist
        assert test_instance.id is not None
        assert isinstance(test_instance.created_at, datetime)
        assert isinstance(test_instance.updated_at, datetime)


# Test to_dict method converts model to dictionary
def test_base_model_to_dict(app, reset_db) -> None:
    with app.app_context():
        db.create_all()
        
        test_instance = SampleModel(name="test", value=42)
        db.session.add(test_instance)
        db.session.commit()
        
        result = test_instance.to_dict()
        
        assert isinstance(result, dict)
        assert result["id"] == test_instance.id
        assert result["name"] == "test"
        assert result["value"] == 42
        assert "created_at" in result
        assert "updated_at" in result


# Test update method updates model fields
def test_base_model_update(app, reset_db) -> None:
    with app.app_context():
        db.create_all()
        
        test_instance = SampleModel(name="test", value=42)
        db.session.add(test_instance)
        db.session.commit()
        
        # Update fields
        test_instance.update(name="updated", value=100)
        
        assert test_instance.name == "updated"
        assert test_instance.value == 100
        
        # Update should not affect non-existent fields
        test_instance.update(nonexistent="should_not_set")
        assert not hasattr(test_instance, "nonexistent")


# Test __repr__ method returns string representation
def test_base_model_repr(app, reset_db) -> None:
    with app.app_context():
        db.create_all()
        
        test_instance = SampleModel(name="test", value=42)
        db.session.add(test_instance)
        db.session.commit()
        
        repr_str = repr(test_instance)
        
        assert isinstance(repr_str, str)
        assert "SampleModel" in repr_str
        assert str(test_instance.id) in repr_str


# Test that updated_at changes when model is updated
def test_base_model_updated_at(app, reset_db) -> None:
    with app.app_context():
        db.create_all()
        
        test_instance = SampleModel(name="test", value=42)
        db.session.add(test_instance)
        db.session.commit()
        
        original_updated_at = test_instance.updated_at
        
        # Wait a tiny bit and update
        import time
        time.sleep(0.01)
        
        test_instance.update(value=100)
        db.session.commit()
        
        # updated_at should have changed
        assert test_instance.updated_at > original_updated_at

