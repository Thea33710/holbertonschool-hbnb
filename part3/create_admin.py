from app import create_app, db
from app.models.user import User

app = create_app()
app.app_context().push()

admin = User.query.filter_by(email="admin@hbnb.com").first()
admin.is_admin = True
db.session.commit()
print("Admin mis à jour !")
