from app.models.base_model import BaseModel

"""Amenity model definition."""


class Amenity(BaseModel):
    """The amenity class based on the BaseModel."""
    all_amenities = []

    def __init__(self, name):
        """Constructor of the Amenity class."""
        super().__init__()
        if any(a.name == name for a in Amenity.all_amenities):
            raise ValueError(f"Amenity '{name}' already exists.")

        self.name = name
        Amenity.all_amenities.append(self)

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
