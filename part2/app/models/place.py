from app.models.base_model import BaseModel
from app.models.user import User

"""Place model definition."""


class Place(BaseModel):
    """The place class based on the BaseModel."""
    all_places = []

    def __init__(self, title, description, price, latitude, longitude, owner):
        """Constructor of the Place class."""
        super().__init__()

        if not title or not isinstance(title, str) or len(title) > 100:
            raise ValueError(
                "title must be a non-empty string up to 100 characters."
            )

        if price is None or not isinstance(price, (int, float)) or price <= 0:
            raise ValueError(
                "The price must be a positive number."
            )

        if (
            latitude is None
            or not isinstance(latitude, (int, float))
            or not (-90.0 <= latitude <= 90.0)
        ):
            raise ValueError(
                "Latitude must be a number between -90.0 and 90.0."
            )

        if (
            longitude is None
            or not isinstance(longitude, (int, float))
            or not (-180.0 <= longitude <= 180.0)
        ):
            raise ValueError(
                "Longitude must be a number between -180.0 and 180.0."
            )

        if not isinstance(owner, User):
            raise TypeError("Owner must be a valid User instance.")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

        Place.all_places.append(self)

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
