from .basemodel import BaseModel
from .place import Place
from .user import User

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    # ----------------- Text -----------------
    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if not value:
            raise ValueError("Text cannot be empty")
        if not isinstance(value, str):
            raise TypeError("Text must be a string")
        self.__text = value

    # ----------------- Rating -----------------
    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        super().is_between('rating', value, 1, 5)  # 1 ≤ rating ≤ 5
        self.__rating = value

    # ----------------- Place -----------------
    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, value):
        if not isinstance(value, Place):
            raise TypeError("Place must be a Place instance")
        self.__place = value

    # ----------------- User -----------------
    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise TypeError("User must be a User instance")
        self.__user = value

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

    # ----------------- Representation -----------------
    def __repr__(self):
        return f"<Review id={self.id} rating={self.rating} place_id={self.place.id} user_id={self.user.id}>"
