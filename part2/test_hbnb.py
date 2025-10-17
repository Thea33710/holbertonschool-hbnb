#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def print_response(r):
    try:
        data = r.json()
    except Exception:
        data = r.text
    print(f"{r.request.method} {r.url} => {r.status_code}\n{json.dumps(data, indent=2)}\n")

# ---------------- USERS ----------------
def test_users():
    print("=== TEST USERS ===")
    # Correct user
    user_data = {"first_name": "Alice", "last_name": "Smith", "email": "alice@example.com"}
    r = requests.post(f"{BASE_URL}/users/", json=user_data)
    print_response(r)
    user_id = r.json().get("id") if r.status_code == 201 else None

    # Invalid user (missing email)
    r = requests.post(f"{BASE_URL}/users/", json={"first_name": "Bob", "last_name": "Lee"})
    print_response(r)

    # GET all users
    r = requests.get(f"{BASE_URL}/users/")
    print_response(r)
    return user_id

# ---------------- AMENITIES ----------------
def test_amenities():
    print("=== TEST AMENITIES ===")
    amenity_data = {"name": "Wi-Fi"}
    r = requests.post(f"{BASE_URL}/amenities/", json=amenity_data)
    print_response(r)
    amenity_id = r.json().get("id") if r.status_code == 201 else None

    # Invalid amenity (too long name)
    r = requests.post(f"{BASE_URL}/amenities/", json={"name": "A"*60})
    print_response(r)

    # GET all amenities
    r = requests.get(f"{BASE_URL}/amenities/")
    print_response(r)
    return amenity_id

# ---------------- PLACES ----------------
def test_places(owner_id, amenity_id):
    print("=== TEST PLACES ===")
    place_data = {
        "title": "Test Apartment",
        "description": "Nice place",
        "price": 100,
        "latitude": 45.0,
        "longitude": -73.0,
        "owner_id": owner_id,
        "amenities": [amenity_id]
    }
    r = requests.post(f"{BASE_URL}/places/", json=place_data)
    print_response(r)
    place_id = r.json().get("id") if r.status_code == 201 else None

    # Invalid place (negative price)
    invalid_place = place_data.copy()
    invalid_place["price"] = -50
    r = requests.post(f"{BASE_URL}/places/", json=invalid_place)
    print_response(r)

    # GET all places
    r = requests.get(f"{BASE_URL}/places/")
    print_response(r)

    # GET single place
    if place_id:
        r = requests.get(f"{BASE_URL}/places/{place_id}")
        print_response(r)

    # GET non-existing place
    r = requests.get(f"{BASE_URL}/places/nonexistent")
    print_response(r)

    return place_id

# ---------------- REVIEWS ----------------
def test_reviews(user_id, place_id):
    print("=== TEST REVIEWS ===")
    review_data = {"text": "Great stay!", "rating": 5, "user_id": user_id, "place_id": place_id}
    r = requests.post(f"{BASE_URL}/reviews/", json=review_data)
    print_response(r)
    review_id = r.json().get("id") if r.status_code == 201 else None

    # Invalid review (rating out of range)
    invalid_review = {"text": "Bad", "rating": 10, "user_id": user_id, "place_id": place_id}
    r = requests.post(f"{BASE_URL}/reviews/", json=invalid_review)
    print_response(r)

    # GET all reviews
    r = requests.get(f"{BASE_URL}/reviews/")
    print_response(r)

    # GET reviews for place
    r = requests.get(f"{BASE_URL}/places/{place_id}/reviews")
    print_response(r)

    # GET single review
    if review_id:
        r = requests.get(f"{BASE_URL}/reviews/{review_id}")
        print_response(r)

        # GET non-existing review
        r = requests.get(f"{BASE_URL}/reviews/nonexistent")
        print_response(r)

        # PUT update review
        update_data = {"text": "Amazing stay!", "rating": 4, "user_id": user_id, "place_id": place_id}
        r = requests.put(f"{BASE_URL}/reviews/{review_id}", json=update_data)
        print_response(r)

        # PUT invalid update
        invalid_update = {"text": "", "rating": 6, "user_id": user_id, "place_id": place_id}
        r = requests.put(f"{BASE_URL}/reviews/{review_id}", json=invalid_update)
        print_response(r)

        # DELETE review
        r = requests.delete(f"{BASE_URL}/reviews/{review_id}")
        print_response(r)

        # GET deleted review (should 404)
        r = requests.get(f"{BASE_URL}/reviews/{review_id}")
        print_response(r)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    user_id = test_users()
    if not user_id:
        print("No user created. Exiting...")
        exit(1)

    amenity_id = test_amenities()
    place_id = test_places(user_id, amenity_id)
    if not place_id:
        print("No place created. Exiting...")
        exit(1)

    test_reviews(user_id, place_id)
