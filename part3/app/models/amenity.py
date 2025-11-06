from .basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    # ----------------- Name -----------------
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value:
            raise ValueError("Name cannot be empty")
        super().is_max_length('name', value, 50)  # utiliser le nom de l'attribut
        self.__name = value

    # ----------------- Update -----------------
    def update(self, data):
        """Met à jour l'objet en utilisant le setter pour appliquer la validation"""
        if 'name' in data:
            self.name = data['name']
        super().update({k: v for k, v in data.items() if k != 'name'})
        return self

    # ----------------- Serialization -----------------
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    # ----------------- Représentation -----------------
    def __repr__(self):
        return f"<Amenity id={self.id} name={self.name}>"
