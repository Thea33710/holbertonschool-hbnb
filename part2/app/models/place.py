from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review

"""Place model definition."""


class Place(BaseModel):
    """The place class based on the BaseModel."""
    all_places = []

    def __init__(self, title, description, price, latitude, longitude, owner):
        """Constructor of the Place class."""
        super().__init__()

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

        Place.all_places.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str) or len(value) > 100:
            raise ValueError(
                "title must be a non-empty string up to 100 characters."
            )
        self._title = value.strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("Description must be a string.")
        self._description = value.strip() if value else ""

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number.")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be a number between -90.0 and 90.0.")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be a number between -180.0 and 180.0.")
        self._longitude = float(value)

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError("Owner must be a valid User instance.")
        self._owner = value

    def add_review(self, review):
        if not isinstance(review, Review):
            raise TypeError("Review must be a Review instance.")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise TypeError("Amenity must be an Amenity instance.")
        self.amenities.append(amenity)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner.to_json(),
            "amenities": [a.to_json() for a in self.amenities],
            "reviews": [r.to_json() for r in self.reviews]
        }
