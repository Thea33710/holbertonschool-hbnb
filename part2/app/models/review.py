from app.models.base_model import BaseModel

"""Review model definition."""


class Review(BaseModel):
    """The review class based on the BaseModel."""
    all_reviews = []

    def __init__(self, text, rating, place, user):
        """Constructor of the review class."""
        super().__init__()

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.place.add_review(self)

        Review.all_reviews.append(self)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError("Text must be a string.")

        value = value.strip()
        if not value:
            raise ValueError("Text is required.")
        self._text = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        self._rating = value

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        from app.models.place import Place
        if not isinstance(value, Place):
            raise TypeError("Place must be a valid Place instance.")
        if value not in Place.all_places:
            raise ValueError("This place does not exist.")
        self._place = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        from app.models.user import User
        if not isinstance(value, User):
            raise TypeError("User must be a valid User instance.")
        if value not in User.all_users:
            raise ValueError("This user does not exist.")
        self._user = value

    def to_json(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place.id,
            "user_id": self.user.id
        }
