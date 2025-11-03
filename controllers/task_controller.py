from flask import Blueprint, request, jsonify
from models.task_model import TaskModel

# Crear blueprint de tareas
task_bp = Blueprint("task_bp", __name__)

# ✅ Listar todas las tareas
@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    try:
        tasks = TaskModel.list_tasks()
        return jsonify(tasks), 200
    except Exception as e:
        print(f"❌ Error al listar tareas: {e}")
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500


# ✅ Obtener tarea por ID
@task_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    try:
        task = TaskModel.get_task(task_id)
        if task:
            return jsonify(task), 200
        return jsonify({"error": "Tarea no encontrada"}), 404
    except Exception as e:
        print(f"❌ Error al obtener tarea: {e}")
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500


# ✅ Crear nueva tarea
@task_bp.route("/tasks", methods=["POST"])
def create_task():
    try:
        data = request.get_json()
        result = TaskModel.create_task(data)
        status = 201 if result.get("success") else 400
        return jsonify(result), status
    except Exception as e:
        print(f"❌ Error al crear tarea: {e}")
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500


# ✅ Actualizar tarea
@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        data = request.get_json()
        result = TaskModel.update_task(task_id, data)
        status = 200 if result.get("success") else 400
        return jsonify(result), status
    except Exception as e:
        print(f"❌ Error al actualizar tarea: {e}")
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500


# ✅ Eliminar tarea
@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        result = TaskModel.delete_task(task_id)
        status = 200 if result.get("success") else 400
        return jsonify(result), status
    except Exception as e:
        print(f"❌ Error al eliminar tarea: {e}")
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500
