import json
from utils.responses import send_json
from utils.auth_utils import verify_token
from models.task_model import TaskModel


def handle_task_routes(handler, path, method):
    path_parts = path.strip("/").split("/")
    auth_header = handler.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        send_json(handler, {"error": "Token no proporcionado"}, 401)
        return
    
    token = auth_header.split(" ")[1]
    decoded = verify_token(token)

    if "error" in decoded:
        send_json(handler, {"error": decoded["error"]}, 401)
        return
    
    user_id = decoded.get("user_id")


    #----------RUTAS-----------

    if method == "GET":
        tasks = TaskModel.list_tasks(user_id)
        send_json(handler, tasks, 200)

    elif method == "POST":
        content_length = int(handler.headers["Content-Length"])
        post_data = json.loads(handler.rfile.read(content_length))
        result = TaskModel.create_task(user_id, post_data)
        send_json(handler, result, 201 if result.get("success") else 400)

    elif method == "PUT":
        if len(path_parts) == 2 and path_parts[0] == "tasks":
            task_id = int(path_parts[1])
            content_length = int(handler.headers.get('Content-Length', 0))
            if content_length == 0:
                send_json(handler, {"error": "Cuerpo vacío"}, 400)
                return

            put_data = json.loads(handler.rfile.read(content_length))

            result = TaskModel.update_task(user_id, task_id, put_data)
            send_json(handler, result, 200 if result.get("success") else 400)
        else:
            send_json(handler, {"error": "Ruta no encontrada"}, 404)


    elif method == "DELETE":
        if len(path_parts) == 2 and path_parts[0] == "tasks":
            task_id = path_parts[1]
            result = TaskModel.delete_task(user_id, task_id)
            send_json(handler, result, 200 if result.get("success") else 400)
        else:
            send_json(handler, {"error": "Ruta no encontrada"}, 404)

    else:
        send_json(handler, {"error": "Método no permitido"}, 405)