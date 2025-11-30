from app import create_app, db

app = create_app()

with app.app_context():
    # Supprime toutes les tables
    db.drop_all()
    
    # Recrée toutes les tables avec le nouveau schéma
    db.create_all()
    
    print("✅ Base de données recréée avec succès !")
