from app.models.base_model import BaseModel

"""Amenity model definition."""


class Amenity(BaseModel):
    """The amenity class based on the BaseModel."""
    def __init__(self, name):
        """Constructor of the Amenity class."""
        super().__init__()

        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError(
                "Amenity name must be a non-empty string "
                + "of maximum 50 characteres."
            )
        self._name = value

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }
