from app import db
from .basemodel import BaseModel
from .place import Place
from .user import User
import uuid

class Review(BaseModel):
    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    place = db.relationship('Place', back_populates='reviews')
    user = db.relationship('User', backref='reviews')

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    # ----------------- Update -----------------
    def update(self, data):
        if 'text' in data:
            self.text = data['text']
        if 'rating' in data:
            self.rating = data['rating']
        super().update({k: v for k, v in data.items() if k not in ['text', 'rating']})
        return self

    # ----------------- Serialization -----------------
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id,
            'user_id': self.user.id
        }

    def to_dict_full(self):
        """Full representation with user and place details."""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place': self.place.to_dict() if hasattr(self.place, 'to_dict') else None,
            'user': self.user.to_dict() if hasattr(self.user, 'to_dict') else None
        }

    # ----------------- Representation -----------------
    def __repr__(self):
        return f"<Review id={self.id} rating={self.rating} place_id={self.place.id} user_id={self.user.id}>"
