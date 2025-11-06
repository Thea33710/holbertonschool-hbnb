from .basemodel import BaseModel
from .user import User

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []   # Liste des reviews
        self.amenities = [] # Liste des amenities

    # ----------------- Title -----------------
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Title cannot be empty")
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        super().is_max_length('title', value, 100)
        self.__title = value

    # ----------------- Price -----------------
    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("Price must be a float")
        value = float(value)
        if value < 0:
            raise ValueError("Price must be positive.")
        self.__price = value

    # ----------------- Latitude -----------------
    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("Latitude must be a float")
        value = float(value)
        super().is_between("latitude", value, -90, 90)
        self.__latitude = value

    # ----------------- Longitude -----------------
    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("Longitude must be a float")
        value = float(value)
        super().is_between("longitude", value, -180, 180)
        self.__longitude = value

    # ----------------- Owner -----------------
    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError("Owner must be a User instance")
        self.__owner = value

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
