from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User

"""Review model definition."""


class Review(BaseModel):
    """The review class based on the BaseModel."""
    all_reviews = []

    def __init__(self, text, rating, place, user):
        """Constructor of the review class."""
        super().__init__()

        if not isinstance(text, str):
            raise TypeError("Text must be a string.")

        text = text.strip()
        if not text:
            raise ValueError("Text is required.")

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating required an integer between 1 and 5.")

        if not isinstance(place, Place):
            raise TypeError("Place must be a valid place instance.")

        if place not in Place.all_places:
            raise ValueError("This place does not exist.")

        if not isinstance(user, User):
            raise TypeError("User must be a valid user instance.")

        if user not in User.all_users:
            raise ValueError("This user does not exist.")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        Review.all_reviews.append(self)
