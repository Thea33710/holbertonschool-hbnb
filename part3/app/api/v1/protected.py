from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

"""espace logic dans le quelle est stocker /protected"""
api = Namespace('protected', description='Protected endpoint')


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    # L’utilisateur doit être connecté avec un JWT
    def get(self):
        """Un point de terminaison protégé qui nécessite un jeton JWT valide"""
        print("jwt------")
        print(get_jwt_identity())
        # On récupère l’identité de l’utilisateur depuis le token
        current_user = get_jwt_identity()

        return {'message': f'Hello, user {current_user}'}, 200
