from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# ----- Models -----
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# ----- Helpers -----
def is_admin():
    claims = get_jwt()
    return claims.get('is_admin', False)

# ----- List & Create Reviews -----
@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @jwt_required()
    def post(self):
        """Create a new review"""
        current_user_id = get_jwt_identity()
        data = api.payload

        place = facade.get_place(data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404

        user = facade.get_user(current_user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if place.owner.id == current_user_id:
            return {'error': 'You cannot review your own place.'}, 403

        existing_review = [r for r in place.reviews if r.user.id == current_user_id]
        if existing_review:
            return {'error': 'You have already reviewed this place.'}, 400

        # Validate rating
        if not (1 <= data['rating'] <= 5):
            return {'error': 'Rating must be between 1 and 5.'}, 400

        try:
            data['user'] = user
            new_review = facade.create_review(data)
            place.add_review(new_review)
            return new_review.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    def get(self):
        """List all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

# ----- Get, Update, Delete a Review -----
@api.route('/<review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @jwt_required()
    def put(self, review_id):
        """Update a review (owner only)"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if review.user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        data = api.payload
        if 'rating' in data and not (1 <= data['rating'] <= 5):
            return {'error': 'Rating must be between 1 and 5.'}, 400

        try:
            facade.update_review(review_id, data)
            return review.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400

    @jwt_required()
    def delete(self, review_id):
        """Delete a review (owner or admin)"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if review.user.id != current_user_id and not is_admin():
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
