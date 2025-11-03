from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from utils.auth_utils import generate_token

# Crear blueprint de usuarios
user_bp = Blueprint("user_bp", __name__)

# ✅ Listar todos los usuarios
@user_bp.route("/users", methods=["GET"])
def get_users():
    try:
        users = UserModel.list_users()
        return jsonify(users), 200
    except Exception as e:
        print(f"❌ Error al listar usuarios: {e}")
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500


# ✅ Obtener usuario por ID
@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = UserModel.get_user(user_id)
        if user:
            return jsonify(user), 200
        return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        print(f"❌ Error al obtener usuario: {e}")
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500


# ✅ Crear usuario
@user_bp.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        result = UserModel.create_user(data)
        status = 201 if result.get("success") else 400
        return jsonify(result), status
    except Exception as e:
        print(f"❌ Error al crear usuario: {e}")
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500


# ✅ Actualizar usuario
@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.get_json()
        result = UserModel.update_user(user_id, data)
        status = 200 if result.get("success") else 400
        return jsonify(result), status
    except Exception as e:
        print(f"❌ Error al actualizar usuario: {e}")
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500


# ✅ Eliminar usuario
@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        result = UserModel.delete_user(user_id)
        status = 200 if result.get("success") else 400
        return jsonify(result), status
    except Exception as e:
        print(f"❌ Error al eliminar usuario: {e}")
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500


# ✅ Login de usuario
@user_bp.route("/login", methods=["POST"])
def login_user():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        auth_result = UserModel.authenticate(email, password)
        if "error" in auth_result:
            return jsonify(auth_result), 401

        user_id = auth_result["user"]["id"]
        token = generate_token(user_id)
        return jsonify({"success": True, "token": token}), 200
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500
