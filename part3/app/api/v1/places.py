from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

places_api = Namespace('places', description='Place operations')

# ----- Models -----
amenity_model = places_api.model('PlaceAmenity', {
    'id': fields.String(required=True, description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

place_model = places_api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities IDs")
})

# ----- Helpers -----
def is_admin():
    claims = get_jwt()
    return claims.get('is_admin', False)

def validate_place_data(data):
    """Validate required fields and types"""
    required_fields = ['title', 'price', 'latitude', 'longitude', 'amenities']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing field: {field}")
        if data[field] is None:
            raise ValueError(f"Field {field} cannot be None")

    # Type checks
    if not isinstance(data['title'], str) or len(data['title']) > 100:
        raise TypeError("Title must be a string with max 100 chars")
    if not isinstance(data['price'], (int, float)) or data['price'] < 0:
        raise ValueError("Price must be a positive number")
    if not isinstance(data['latitude'], float) or not -90 <= data['latitude'] <= 90:
        raise ValueError("Latitude must be float between -90 and 90")
    if not isinstance(data['longitude'], float) or not -180 <= data['longitude'] <= 180:
        raise ValueError("Longitude must be float between -180 and 180")
    if not isinstance(data['amenities'], list):
        raise TypeError("Amenities must be a list of IDs")

# ----- List & Create Places -----
@places_api.route('/')
class PlaceList(Resource):
    @places_api.expect(place_model)
    @jwt_required()
    def post(self):
        """Create a new place (owner = current user)"""
        current_user_id = get_jwt_identity()
        user = facade.get_user(current_user_id)
        if not user:
            return {'error': 'User not found'}, 404

        place_data = places_api.payload
        try:
            validate_place_data(place_data)
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

        # Get amenity objects
        amenities = []
        for a_id in place_data['amenities']:
            amenity = facade.get_amenity(a_id)
            if not amenity:
                return {'error': f"Amenity {a_id} not found"}, 400
            amenities.append(amenity)
        place_data['amenities'] = amenities
        place_data['owner'] = user

        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict_list(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    def get(self):
        """List all places"""
        places = facade.get_all_places()
        return [p.to_dict_list() for p in places], 200

# ----- Get, Update & Delete Place -----
@places_api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict_list(), 200

    @places_api.expect(place_model)
    @jwt_required()
    def put(self, place_id):
        """Update place (owner or admin)"""
        current_user_id = get_jwt_identity()
        admin = is_admin()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404
        if not admin and place.owner.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        update_data = places_api.payload
        # Optional: validate only provided fields
        try:
            if 'title' in update_data:
                if not isinstance(update_data['title'], str) or len(update_data['title']) > 100:
                    raise TypeError("Title must be string max 100 chars")
            if 'price' in update_data:
                if not isinstance(update_data['price'], (int, float)) or update_data['price'] < 0:
                    raise ValueError("Price must be positive")
            if 'latitude' in update_data:
                if not isinstance(update_data['latitude'], float) or not -90 <= update_data['latitude'] <= 90:
                    raise ValueError("Latitude must be float between -90 and 90")
            if 'longitude' in update_data:
                if not isinstance(update_data['longitude'], float) or not -180 <= update_data['longitude'] <= 180:
                    raise ValueError("Longitude must be float between -180 and 180")
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

        try:
            facade.update_place(place_id, update_data)
            return place.to_dict_list(), 200
        except Exception as e:
            return {'error': str(e)}, 400

    @jwt_required()
    def delete(self, place_id):
        """Delete place (owner or admin)"""
        current_user_id = get_jwt_identity()
        admin = is_admin()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404
        if not admin and place.owner.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.delete_place(place_id)
            return {'message': 'Place deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

# ----- Add Amenities to Place -----
@places_api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @places_api.expect([amenity_model])
    @jwt_required()
    def post(self, place_id):
        current_user_id = get_jwt_identity()
        admin = is_admin()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404
        if not admin and place.owner.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        amenities_data = places_api.payload
        if not amenities_data:
            return {'error': 'Invalid input data'}, 400

        for a_item in amenities_data:
            amenity = facade.get_amenity(a_item['id'])
            if not amenity:
                return {'error': f"Amenity {a_item['id']} not found"}, 400
            if amenity not in place.amenities:
                place.add_amenity(amenity)

        facade.update_place(place_id, {'amenities': place.amenities})
        return place.to_dict_list(), 200

# ----- List Reviews for a Place -----
@places_api.route('/<place_id>/reviews/')
class PlaceReviewList(Resource):
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return [r.to_dict() for r in place.reviews], 200
