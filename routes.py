from controllers.user_controller import (
    GET_USERS, GET_USER_BY_ID, CREATE_USER, UPDATE_USER, DELETE_USER
)
from controllers.task_controller import (
    GET_TASKS, GET_TASK_BY_ID, CREATE_TASK, UPDATE_TASK, DELETE_TASK
)


def handle_request(path, method, body=None, query_params=None):
    """
    Define las rutas disponibles y ejecuta la función correspondiente
    según el path y método HTTP.
    """

    # -----------------------------
    # RUTAS DE USUARIOS
    # -----------------------------
    if path == "/users" and method == "GET":
        return GET_USERS()

    elif path.startswith("/users/") and method == "GET":
        user_id = int(path.split("/")[-1])
        return GET_USER_BY_ID(user_id)

    elif path == "/users" and method == "POST":
        return CREATE_USER(body)

    elif path.startswith("/users/") and method == "PUT":
        user_id = int(path.split("/")[-1])
        return UPDATE_USER(user_id, body)

    elif path.startswith("/users/") and method == "DELETE":
        user_id = int(path.split("/")[-1])
        return DELETE_USER(user_id)

    # -----------------------------
    # RUTAS DE TAREAS
    # -----------------------------
    elif path == "/tasks" and method == "GET":
        return GET_TASKS()

    elif path.startswith("/tasks/") and method == "GET":
        task_id = int(path.split("/")[-1])
        return GET_TASK_BY_ID(task_id)

    elif path == "/tasks" and method == "POST":
        return CREATE_TASK(body)

    elif path.startswith("/tasks/") and method == "PUT":
        task_id = int(path.split("/")[-1])
        return UPDATE_TASK(task_id, body)

    elif path.startswith("/tasks/") and method == "DELETE":
        task_id = int(path.split("/")[-1])
        return DELETE_TASK(task_id)

    # -----------------------------
    # RUTA NO ENCONTRADA
    # -----------------------------
    else:
        return {"status": 404, "message": "Ruta no encontrada"}
