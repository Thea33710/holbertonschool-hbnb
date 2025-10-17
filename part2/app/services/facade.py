from app.models.amenity import Amenity
from app.models.user import User
from app.models.review import Review
from app.models.place import Place
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, new_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        for key, value in new_data.items():
            setattr(user, key, value)
        self.user_repo.update(user_id, user)
        return user

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def create_amenity(self, data):
        name = data.get("name")
        if not name or not isinstance(name, str) or len(name) > 50:
            raise ValueError("Amenity name must be a non-empty string of max 50 chars")
    
        # Vérifier si déjà existant
        if any(a.name == name for a in self.amenity_repo.get_all()):
            raise ValueError("Amenity already exists")
    
        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)  # AJOUTER DANS LE REPOSITORY
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, new_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        for key, value in new_data.items():
            setattr(amenity, key, value)

        self.amenity_repo.update(amenity_id, amenity.to_json())
        
        return amenity

    def create_place(self, place_data):
        owner = self.user_repo.get(place_data.get("owner_id"))
        if not owner:
            raise ValueError("Owner not found")

        amenities = []
        for amenity_id in place_data.get('amenities', []):
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                amenities.append(amenity)

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )

        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, new_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        try:
            # --- 1. Handle owner change ---
            if "owner_id" in new_data:
                owner = self.user_repo.get(new_data["owner_id"])
                if not owner:
                    raise ValueError(f"Owner with ID {new_data['owner_id']} not found")
                place.owner = owner

            # --- 2. Handle amenities list ---
            if "amenities" in new_data:
                amenity_ids = new_data["amenities"]
                if not isinstance(amenity_ids, list):
                    raise TypeError("amenities must be a list of amenity IDs")

                amenities = []
                for amenity_id in amenity_ids:
                    amenity = self.amenity_repo.get(amenity_id)
                    if not amenity:
                        raise ValueError(f"Amenity with ID {amenity_id} not found")
                    amenities.append(amenity)
                place.amenities = amenities

            # --- 3. Handle basic attributes ---
            for key in ["title", "description", "price", "latitude", "longitude"]:
                if key in new_data:
                    setattr(place, key, new_data[key])

            # --- 4. Save updated object ---
            self.place_repo.update(place_id, place)
            return place

        except Exception as e:
            # On remonte l’erreur pour que l’API Flask la renvoie en 400
            raise e

    def create_review(self, review_data):
        user = self.get_user(review_data.get("user_id"))
        place = self.get_place(review_data.get("place_id"))
    
        if not user or not place:
            raise ValueError("Invalid user_id or place_id")

        review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            user=user,
            place=place
        )
        return review

    def get_review(self, review_id):
        for review in Review.all_reviews:
            if review.id == review_id:
                return review
        return None

    def get_all_reviews(self):
        return Review.all_reviews

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        if "text" in review_data:
            review.text = review_data["text"]
        if "rating" in review_data:
            review.rating = review_data["rating"]

        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False

        if review.place and review in review.place.reviews:
            review.place.reviews.remove(review)

        Review.all_reviews.remove(review)
        return True
