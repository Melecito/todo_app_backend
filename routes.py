from controllers.user_controller import handle_user_routes
from controllers.task_controller import handle_task_routes

def handle_request(handler, path, method):
    """
    Redirige las rutas al controlador correspondiente.
    """
    if path.startswith("/users") or path == "/login":
        return handle_user_routes(handler, path, method)
    elif path.startswith("/tasks"):
        return handle_task_routes(handler, path, method)
    else:
        from utils.responses import send_json
        send_json(handler, {"error": "Ruta no encontrada"}, 404)
