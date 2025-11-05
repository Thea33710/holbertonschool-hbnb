from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(409, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new user (Admins only)"""
        jwt_data = get_jwt()
        is_admin = jwt_data.get("is_admin", False)
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 409

        if 'password' not in user_data:
            return {'error': 'Password is required'}, 400

        password = user_data.pop('password')
        try:
            new_user = facade.create_user(user_data)
            new_user.hash_password(password)
            return new_user.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def get(self):
        """Retrieve all users (Admins only)"""
        jwt_data = get_jwt()
        is_admin = jwt_data.get("is_admin", False)
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403

        users = facade.get_users()
        return [user.to_dict() for user in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update user information"""
        current_user_id = get_jwt_identity()
        jwt_data = get_jwt()
        is_admin = jwt_data.get("is_admin", False)

        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if not is_admin:
            if user_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403
            if 'email' in user_data or 'password' in user_data:
                return {'error': 'You cannot modify email or password'}, 400

        if is_admin and 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        try:
            facade.update_user(user_id, user_data)
            return {'message': 'User updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
