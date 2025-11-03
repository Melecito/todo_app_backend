from flask import request, jsonify
from models.user_model import UserModel
from utils.auth_utils import generate_token


def user_routes(app):
    """
    Registra todas las rutas relacionadas con usuarios en Flask.
    """

    @app.route('/api/users', methods=['GET'])
    def get_users():
        users = UserModel.list_users()
        return jsonify(users), 200

    @app.route('/api/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = UserModel.get_user(user_id)
        if user:
            return jsonify(user), 200
        return jsonify({"error": "Usuario no encontrado"}), 404

    @app.route('/api/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        result = UserModel.create_user(data)
        return jsonify(result), 201 if result.get("success") else 400

    @app.route('/api/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        data = request.get_json()
        result = UserModel.update_user(user_id, data)
        return jsonify(result), 200 if result.get("success") else 400

    @app.route('/api/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        result = UserModel.delete_user(user_id)
        return jsonify(result), 200 if result.get("success") else 400

    @app.route('/api/login', methods=['POST'])
    def login_user():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        auth_result = UserModel.authenticate(email, password)
        if "error" in auth_result:
            return jsonify(auth_result), 401
        else:
            user_id = auth_result["user"]["id"]
            token = generate_token(user_id)
            return jsonify({"success": True, "token": token}), 200
