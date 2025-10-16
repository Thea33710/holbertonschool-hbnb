from app.models.base_model import BaseModel

"""Amenity model definition."""


class Amenity(BaseModel):
    """The amenity class based on the BaseModel."""
    def __init__(self, name):
        """Constructor of the Amenity class."""
        super().__init__()

        if not name or not isinstance(name, str) or len(name) > 50:
            raise ValueError(
                "Amenity name must be a non-empty string "
                + "of maximum 50 characteres."
            )

        self.name = name

def to_dict(self):
        """Return a dictionary representation of the Amenity."""
        return {
            "id": self.id,
            "name": self.name
        }
