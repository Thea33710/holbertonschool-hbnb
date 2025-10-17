from app.models.base_model import BaseModel

"""User model definition."""


class User(BaseModel):
    """The User class based on the BaseModel."""
    all_users = []

    def __init__(self, first_name, last_name, email, is_admin=False):
        """Constructor of the User class."""
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        User.all_users.append(self)

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("First name must be a string.")

        value = value.strip()
        if not value or len(value) > 50:
            raise ValueError(
                "First name must be a non-empty string up to 50 characters."
            )
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Last name must be a string.")

        value = value.strip()
        if not value or len(value) > 50:
            raise ValueError(
                "Last name must be a non-empty string up to 50 characters."
            )
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string.")

        value = value.strip()
        if not value:
            raise ValueError("Email must not be empty.")

        if (
            "@" not in value
            or not (value.endswith(".fr") or value.endswith(".com"))
        ):
            raise ValueError("Invalid email format.")

        for user in User.all_users:
            if user.email == value:
                raise ValueError("Email must be unique.")

        self._email = value

    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }
