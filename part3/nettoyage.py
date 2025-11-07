from app import create_app, db
from sqlalchemy import text
import uuid

app = create_app()  # créer l'application Flask

with app.app_context():  # ouvrir le contexte
    # ------------------------------
    # 1️⃣ Supprimer les anciennes tables
    # ------------------------------
    tables = ["Place_Amenity", "Review", "Place", "Amenity", "User"]
    for table in tables:
        db.session.execute(text(f"DROP TABLE IF EXISTS {table}"))
    db.session.commit()
    print("Anciennes tables supprimées.")

    # ------------------------------
    # 2️⃣ Créer les nouvelles tables
    # ------------------------------
    db.session.execute(text("""
    CREATE TABLE IF NOT EXISTS users (
        id CHAR(36) PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        email VARCHAR(255) UNIQUE,
        password VARCHAR(255),
        is_admin BOOLEAN DEFAULT FALSE
    );
    """))

    db.session.execute(text("""
    CREATE TABLE IF NOT EXISTS places (
        id CHAR(36) PRIMARY KEY,
        title VARCHAR(255),
        description TEXT,
        price DECIMAL(10, 2),
        latitude FLOAT,
        longitude FLOAT,
        owner_id CHAR(36),
        FOREIGN KEY (owner_id) REFERENCES users(id)
    );
    """))

    db.session.execute(text("""
    CREATE TABLE IF NOT EXISTS reviews (
        id CHAR(36) PRIMARY KEY,
        text TEXT,
        rating INT CHECK (rating >= 1 AND rating <= 5),
        user_id CHAR(36),
        place_id CHAR(36),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (place_id) REFERENCES places(id),
        CONSTRAINT unique_review_place UNIQUE (user_id, place_id)
    );
    """))

    db.session.execute(text("""
    CREATE TABLE IF NOT EXISTS amenities (
        id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """))

    db.session.execute(text("""
    CREATE TABLE IF NOT EXISTS Place_Amenity (
        place_id CHAR(36),
        amenity_id CHAR(36),
        PRIMARY KEY (place_id, amenity_id),
        FOREIGN KEY (place_id) REFERENCES places(id),
        FOREIGN KEY (amenity_id) REFERENCES amenities(id)
    );
    """))

    db.session.commit()
    print("Nouvelles tables créées.")

    # ------------------------------
    # 3️⃣ Insérer admin et amenities
    # ------------------------------
    admin_id = "36c9050e-ddd3-4c3b-9731-9f487208bbc1"
    admin_email = "admin@hbnb.com"
    admin_pw_hash = "$2b$12$VdHyFNE57jk1BhkhiJN0/O8fvaBiC9GtBMROr6rMD/6wpoQ0hLKs6"  # hash de "admin123"

    db.session.execute(text("""
    INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin)
    VALUES (:id, :first, :last, :email, :pw, TRUE)
    """), {"id": admin_id, "first": "Admin", "last": "HBnB", "email": admin_email, "pw": admin_pw_hash})

    amenities_list = [
        (str(uuid.uuid4()), "WiFi"),
        (str(uuid.uuid4()), "Swimming Pool"),
        (str(uuid.uuid4()), "Air Conditioning")
    ]

    for a_id, name in amenities_list:
        db.session.execute(text("""
        INSERT OR IGNORE INTO amenities (id, name)
        VALUES (:id, :name)
        """), {"id": a_id, "name": name})

    db.session.commit()
    print("Admin et amenities insérés avec succès.")
