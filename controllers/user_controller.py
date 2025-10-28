import json
from models.user_model import UserModel
from utils.responses import send_json
from utils.auth_utils import generate_token


def handle_user_routes(handler, path, method):
    path_parts = path.strip("/").split("/")

    if method == "GET":
        if path == "/":
            users = UserModel.list_users()
            send_json(handler, users, 200)
        elif len(path_parts) == 2 and path_parts[0] == "users":
            user = UserModel.get_user(path_parts[1])
            if user:
                send_json(handler, user, 200)
            else:
                send_json(handler, {"error": "Usuario no encontrado"}, 404)
        else:
            send_json(handler, {"error": "Ruta no encontrada"}, 404) 

    elif method == "POST":
        if path == "/users":
            content_length = int(handler.headers['Content-Length'])
            post_data = json.loads(handler.rfile.read(content_length))
            result = UserModel.create_user(post_data)
            status_code = 201 if result.get("success") else 400
            send_json(handler, result, status_code)


        elif path == "/login":
            content_length = int(handler.headers['Content-Length'])
            post_data = json.loads(handler.rfile.read(content_length)) 
            email = post_data.get("email")
            password = post_data.get("password")

            auth_result = UserModel.authenticate(email, password)
            if "error" in auth_result:
                send_json(handler, auth_result, 401)
            else:
                user_id = auth_result["user"]["id"]
                token = generate_token(user_id)
                send_json(handler, {"success": True, "token": token}, 200)

        else:
            send_json(handler, {"error": "Ruta no encontrada"}, 404)

    elif method == "PUT":
        if len(path_parts) == 2 and path_parts[0] == "users":
            user_id = path_parts[1]
            content_length = int(handler.headers['Content-Length'])
            put_data = json.loads(handler.rfile.read(content_length))

            result = UserModel.update_user(user_id, put_data)
            send_json(handler, result, 200 if result.get("success") else 400)
        else:
            send_json(handler, {"error": "Ruta no encontrada"}, 404)

    elif method == "DELETE":
        if len(path_parts) == 2 and path_parts[0] == "users":
            result = UserModel.delete_user(path_parts[1])
            send_json(handler, result, 200 if result.get("success") else 400)
        else:
            send_json(handler, {"error": "Ruta no encontrada"}, 404)