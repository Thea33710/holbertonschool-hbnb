#!/usr/bin/env python3
"""
Script COMPLET pour créer toutes les données de test :
- Utilisateurs
- Places avec images
- Équipements (amenities)
- Avis (reviews)
"""

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

# Configuration
PLACES_DATA = [
    {
        "title": "Appartement à Arcachon",
        "description": "Charmant appartement près du port, pour ballade et moment de détente.",
        "price": 90.0,
        "latitude": 44.6534,
        "longitude": -1.1659,
        "amenities": ["WiFi", "Parking", "TV", "Cuisine équipée"],
        "reviews": [
            {"comment": "Super appartement ! Très bien situé près du port.", "rating": 5},
            {"comment": "Très agréable, je recommande vivement.", "rating": 5}
        ]
    },
    {
        "title": "Maison à Bordeaux",
        "description": "Maison située dans quartier calme près des commerces, place de parking privée",
        "price": 105.0,
        "latitude": 44.8378,
        "longitude": -0.5792,
        "amenities": ["WiFi", "Parking", "Jardin", "Barbecue"],
        "reviews": [
            {"comment": "Maison spacieuse et confortable. Le jardin est un vrai plus.", "rating": 4},
            {"comment": "Bon séjour, quartier calme mais un peu excentré.", "rating": 4}
        ]
    },
    {
        "title": "Maison à Agen",
        "description": "Maison près du centre et de l'église, ballade et randonnées et barbecue",
        "price": 60.0,
        "latitude": 44.2034,
        "longitude": 0.6164,
        "amenities": ["WiFi", "Barbecue", "Parking", "Jardin"],
        "reviews": [
            {"comment": "Rapport qualité/prix excellent ! Parfait pour un weekend.", "rating": 5},
            {"comment": "Maison simple mais tout le nécessaire est là.", "rating": 4}
        ]
    },
    {
        "title": "Appartement à La Rochelle",
        "description": "Charmant appartement près du vieux port, possédant un balcon, proche de tous les commerces.",
        "price": 75.0,
        "latitude": 46.1591,
        "longitude": -1.1520,
        "amenities": ["WiFi", "Balcon", "TV", "Cuisine équipée"],
        "reviews": [
            {"comment": "Emplacement idéal pour visiter La Rochelle !", "rating": 5},
            {"comment": "Appartement propre et bien équipé. Le balcon est top.", "rating": 4}
        ]
    },
    {
        "title": "Appartement à Limoges",
        "description": "Appartement calme, situé en centre ville, avec la ligne de bus à proximité.",
        "price": 65.0,
        "latitude": 45.8336,
        "longitude": 1.2611,
        "amenities": ["WiFi", "TV", "Cuisine équipée", "Parking"],
        "reviews": [
            {"comment": "Très bien situé, accès facile aux transports.", "rating": 4},
            {"comment": "Calme et confortable, parfait pour un séjour professionnel.", "rating": 4}
        ]
    }
]

def create_test_users(app):
    """
    Crée 3 utilisateurs de test
    """
    print("=" * 70)
    print("👥 CRÉATION DES UTILISATEURS")
    print("=" * 70)
    print()
    
    with app.app_context():
        users_data = [
            {
                "email": "test@hbnb.com",
                "password": "Test1234!",
                "first_name": "Jean",
                "last_name": "Dupont",
                "is_admin": False
            },
            {
                "email": "marie@hbnb.com",
                "password": "Marie1234!",
                "first_name": "Marie",
                "last_name": "Martin",
                "is_admin": False
            },
            {
                "email": "admin@hbnb.com",
                "password": "Admin1234!",
                "first_name": "Admin",
                "last_name": "HBNB",
                "is_admin": True
            }
        ]
        
        created_count = 0
        
        for user_data in users_data:
            # Vérifie si l'utilisateur existe déjà
            existing_user = User.query.filter_by(email=user_data['email']).first()
            
            if existing_user:
                print(f"   ℹ️  {user_data['email']} existe déjà")
                created_count += 1
            else:
                try:
                    user = User(
                        email=user_data['email'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        password=user_data['password']
                    )
                    
                    db.session.add(user)
                    db.session.flush()  # Pour obtenir l'ID
                    
                    print(f"   ✅ {user_data['email']} créé (ID: {user.id})")
                    created_count += 1
                    
                except Exception as e:
                    print(f"   ❌ Erreur création {user_data['email']}: {e}")
                    continue
        
        db.session.commit()
        print()
        print(f"✅ {created_count} utilisateurs disponibles")
        print()


def create_amenities(app):
    """
    Crée tous les équipements possibles
    """
    print("=" * 70)
    print("🛠️  CRÉATION DES ÉQUIPEMENTS")
    print("=" * 70)
    print()
    
    with app.app_context():
        amenities_list = [
            "WiFi", "Parking", "TV", "Cuisine équipée", 
            "Jardin", "Barbecue", "Balcon", "Climatisation",
            "Lave-linge", "Lave-vaisselle", "Piscine"
        ]
        
        created_count = 0
        
        for amenity_name in amenities_list:
            # Vérifie si l'équipement existe déjà
            amenity = Amenity.query.filter_by(name=amenity_name).first()
            
            if not amenity:
                amenity = Amenity(name=amenity_name)
                db.session.add(amenity)
                db.session.flush()
                print(f"   ✅ {amenity_name} créé")
            else:
                print(f"   ℹ️  {amenity_name} existe déjà")
            
            created_count += 1
        
        db.session.commit()
        print()
        print(f"✅ {created_count} équipements disponibles")
        print()


def create_places_with_data(app):
    """
    Crée les places avec leurs équipements et avis
    """
    print("=" * 70)
    print("🏠 CRÉATION DES PLACES")
    print("=" * 70)
    print()
    
    with app.app_context():
        # ✅ Récupère les users DEPUIS LA DB (pas depuis un paramètre)
        owner = User.query.filter_by(email='test@hbnb.com').first()
        reviewer = User.query.filter_by(email='marie@hbnb.com').first()
        
        if not owner:
            print("❌ Utilisateur propriétaire non trouvé")
            return
        
        if not reviewer:
            reviewer = owner  # Fallback si Marie n'existe pas
        
        created_places = []
        
        for i, place_data in enumerate(PLACES_DATA, 1):
            print(f"[{i}/{len(PLACES_DATA)}] Création de: {place_data['title']}")
            
            try:
                # Crée la place
                place = Place(
                    title=place_data['title'],
                    description=place_data['description'],
                    price=place_data['price'],
                    latitude=place_data['latitude'],
                    longitude=place_data['longitude']
                )
                
                # ✅ Assigne le propriétaire AVANT d'ajouter à la session
                place.owner_id = owner.id
                place.owner = owner  # Assigne aussi la relation
                
                db.session.add(place)
                db.session.flush()  # Pour obtenir l'ID
                
                print(f"   ✅ Place créée (ID: {place.id})")
                
                # Ajoute les équipements
                for amenity_name in place_data.get('amenities', []):
                    # Récupère l'amenity depuis la DB
                    amenity = Amenity.query.filter_by(name=amenity_name).first()
                    if amenity:
                        place.amenities.append(amenity)
                        print(f"      🛠️  Équipement ajouté: {amenity_name}")
                
                # Commit pour que la place soit bien en DB avant d'ajouter les reviews
                db.session.commit()
                
                # Ajoute les avis
                for review_data in place_data.get('reviews', []):
                    review = Review(
                        text=review_data['comment'],
                        rating=review_data['rating'],
                        place=place,      # ✅ Passe l'objet place complet
                        user=reviewer     # ✅ Passe l'objet user complet
                    )
                    
                    db.session.add(review)
                    print(f"      ⭐ Avis ajouté: {review_data['rating']}/5")
                
                db.session.commit()
                created_places.append(place)
                print()
                
            except Exception as e:
                db.session.rollback()
                print(f"   ❌ Erreur: {e}")
                import traceback
                traceback.print_exc()
                print()
                continue
        
        print(f"✅ {len(created_places)} places créées avec succès")
        print()


def display_summary(app):
    """
    Affiche un résumé des données créées
    """
    print("=" * 70)
    print("📊 RÉSUMÉ DES DONNÉES")
    print("=" * 70)
    print()
    
    with app.app_context():
        users_count = User.query.count()
        places_count = Place.query.count()
        amenities_count = Amenity.query.count()
        reviews_count = Review.query.count()
        
        print(f"   👥 {users_count} utilisateurs")
        print(f"   🏠 {places_count} places")
        print(f"   🛠️  {amenities_count} équipements")
        print(f"   ⭐ {reviews_count} avis")
        print()
        
        print("📍 Places disponibles:")
        places = Place.query.all()
        for place in places:
            print(f"   • {place.title} - {place.price}€/nuit")
            print(f"     - {len(place.amenities)} équipements")
            print(f"     - {len(place.reviews)} avis")
        
        print()
        print("👥 Utilisateurs:")
        users = User.query.all()
        for user in users:
            print(f"   • {user.email} ({user.first_name} {user.last_name})")
        
        print()


def main():
    """
    Fonction principale
    """
    print("\n")
    print("=" * 70)
    print("🎉 SETUP COMPLET DES DONNÉES DE TEST")
    print("=" * 70)
    print()
    
    app = create_app()
    
    try:
        # Étape 1 : Créer les utilisateurs
        create_test_users(app)
        
        # Étape 2 : Créer les équipements
        create_amenities(app)
        
        # Étape 3 : Créer les places avec données
        create_places_with_data(app)
        
        # Étape 4 : Afficher le résumé
        display_summary(app)
        
        print("=" * 70)
        print("✅ CONFIGURATION TERMINÉE AVEC SUCCÈS !")
        print("=" * 70)
        print()
        print("💡 Identifiants de test:")
        print("   Email: test@hbnb.com")
        print("   Password: Test1234!")
        print()
        print("   Email: marie@hbnb.com")
        print("   Password: Marie1234!")
        print()
        print("   Email admin: admin@hbnb.com")
        print("   Password: Admin1234!")
        print()
        print("🚀 Tu peux maintenant lancer ton site web !")
        print()
        
    except Exception as e:
        print(f"\n❌ Erreur lors du setup: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
