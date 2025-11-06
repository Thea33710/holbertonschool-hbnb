from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

app = create_app()
app.app_context().push()  # nécessaire pour accéder à db

# Supprimer toutes les données
print("Vider la base de données...")
Review.query.delete()
Place.query.delete()
Amenity.query.delete()
User.query.delete()
db.session.commit()
print("Base vidée avec succès !")
