from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.task_model import TaskModel

# Blueprint para tareas
task_bp = Blueprint("task_bp", __name__)

# ✅ Obtener todas las tareas del usuario autenticado
@task_bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    try:
        user_id = get_jwt_identity()
        tasks = TaskModel.list_tasks(user_id)
        return jsonify(tasks), 200
    except Exception as e:
        print(f"❌ Error al listar tareas: {e}")
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500


# ✅ Obtener una tarea específica
@task_bp.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    try:
        user_id = get_jwt_identity()
        task = TaskModel.get_task(user_id, task_id)
        if task:
            return jsonify(task), 200
        return jsonify({"error": "Tarea no encontrada"}), 404
    except Exception as e:
        print(f"❌ Error al obtener tarea: {e}")
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500


# ✅ Crear una nueva tarea
@task_bp.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data:
            return jsonify({"error": "Faltan datos en la solicitud"}), 400

        result = TaskModel.create_task(user_id, data)
        status = 201 if result.get("success") else 400
        return jsonify(result), status

    except Exception as e:
        print(f"❌ Error al crear tarea: {e}")
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500


# ✅ Actualizar una tarea existente
@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se enviaron datos para actualizar"}), 400

        result = TaskModel.update_task(user_id, task_id, data)
        status = 200 if result.get("success") else 400
        return jsonify(result), status

    except Exception as e:
        print(f"❌ Error al actualizar tarea: {e}")
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500


# ✅ Eliminar una tarea
@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    try:
        user_id = get_jwt_identity()
        result = TaskModel.delete_task(user_id, task_id)
        status = 200 if result.get("success") else 400
        return jsonify(result), status
    except Exception as e:
        print(f"❌ Error al eliminar tarea: {e}")
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500
