from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def update(self, data):
        """Update attributes from a dictionary and refresh updated_at"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def is_max_length(self, name, value, max_length):
        if len(value) > max_length:
            raise ValueError(f"{name} must be {max_length} characters max.") 

    def is_between(self, name, value, min_val, max_val):
        if not min_val < value < max_val:
            raise ValueError(f"{name} must be between {min_val} and {max_val}.")
