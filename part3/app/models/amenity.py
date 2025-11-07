from .basemodel import BaseModel
import uuid
import re
from app import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name

    # ----------------- Update -----------------
    def update(self, data):
        """Met à jour l'objet en utilisant le setter pour appliquer la validation"""
        if 'name' in data:
            self.name = data['name']
        super().update({k: v for k, v in data.items() if k != 'name'})
        return self

    # ----------------- Serialization -----------------
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    # ----------------- Représentation -----------------
    def __repr__(self):
        return f"<Amenity id={self.id} name={self.name}>"
