from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

users_api = Namespace('users', description='User operations')

# Modèle pour l'auto-inscription
user_model = users_api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

# Modèle pour admin
admin_user_model = users_api.model('AdminUser', {
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String(),
    'password': fields.String(),
    'is_admin': fields.Boolean(description="Set admin privileges")
})

# -------- Helper --------
def admin_required():
    claims = get_jwt()
    return claims.get('is_admin', False)

# -------- Admin operations --------

@users_api.route('/admin/users/')
class AdminUserCreate(Resource):
    @users_api.expect(admin_user_model)
    @jwt_required()
    def post(self):
        """Admin can create a normal user or an admin"""
        if not admin_required():
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        password = user_data.pop('password', None)
        if not password:
            return {'error': 'Password is required'}, 400

        new_user = facade.create_user(user_data)
        new_user.hash_password(password)
        return new_user.to_dict(), 201


@users_api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @users_api.expect(admin_user_model)
    @jwt_required()
    def put(self, user_id):
        """Admin can modify any user"""
        if not admin_required:
            return {'error': 'Admin privileges required'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = request.json
        # Empêche la modification du mot de passe via ce endpoint
        if 'password' in data:
            user.hash_password(data.pop('password'))

        try:
            facade.update_user(user_id, data)
            return user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400


# -------- User self-registration & operations --------

@users_api.route('/')
class UserList(Resource):
    @users_api.expect(user_model)
    def post(self):
        """Register a normal user"""
        user_data = request.json
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 409

        new_user = facade.create_user(user_data)
        new_user.hash_password(user_data['password'])
        return new_user.to_dict(), 201

    @jwt_required()
    def get(self):
        """List all users (admin only)"""
        if not admin_required():
            return {'error': 'Admin privileges required'}, 403
        return [u.to_dict() for u in facade.get_users()], 200


@users_api.route('/<user_id>')
class UserResource(Resource):
    def get(self, user_id):
        """Get user details"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @users_api.expect(user_model)
    @jwt_required()
    def put(self, user_id):
        """User can modify their own data"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if str(user_id) != str(current_user_id) and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = request.json
        data.pop('email', None)
        data.pop('password', None)

        if is_admin and 'is_admin' in data:
            user.is_admin = data['is_admin']

        try:
            facade.update_user(user_id, data)
            return user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
