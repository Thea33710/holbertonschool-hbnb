from .basemodel import BaseModel
from .user import User
import re
from app import db
import uuid

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User', backref='places')
    reviews = db.relationship('Review', back_populates='place', cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, backref='places')


    def __init__(self, title, price, latitude, longitude, owner, description=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    # ----------------- Reviews -----------------
    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def delete_review(self, review):
        """Remove a review from the place."""
        self.reviews.remove(review)

    # ----------------- Amenities -----------------
    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    # ----------------- Serialization -----------------
    def to_dict(self):
        """Return a minimal dictionary for API responses."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id
        }

    def to_dict_list(self):
        """Return a full dictionary including owner, amenities, and reviews."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner.to_dict(),
            'amenities': [a.to_dict() if hasattr(a, 'to_dict') else a for a in self.amenities],
            'reviews': [r.to_dict() if hasattr(r, 'to_dict') else r for r in self.reviews]
        }
