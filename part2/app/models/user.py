from app.models.base_model import BaseModel

"""User model definition."""


class User(BaseModel):
    """The User class based on the BaseModel."""
    all_users = []

    def __init__(self, first_name, last_name, email, is_admin=False):
        """Constructor of the User class."""
        super().__init__()

        if not isinstance(first_name, str):
            raise TypeError("First name must be a string.")

        first_name = first_name.strip()
        if not first_name or len(first_name) > 50:
            raise ValueError(
                "First name must be a non-empty string up to 50 characters."
            )

        if not isinstance(last_name, str):
            raise TypeError("Last name must be a string.")

        last_name = last_name.strip()
        if not last_name or len(last_name) > 50:
            raise ValueError(
                "Last name must be a non-empty string up to 50 characters."
            )

        if not isinstance(email, str):
            raise TypeError("Email must be a string.")

        email = email.strip()
        if not email:
            raise ValueError("Email must not be empty.")

        if (
            "@" not in email
            or not (email.endswith(".fr") or email.endswith(".com"))
        ):
            raise ValueError("Invalid email format.")

        for user in User.all_users:
            if user.email == email:
                raise ValueError("Email must be unique.")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        User.all_users.append(self)
