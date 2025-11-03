# routes.py
from controllers.user_controller import user_routes
from controllers.task_controller import task_routes

def register_routes(app):
    """
    Registra todas las rutas del backend en la aplicación Flask.
    """
    user_routes(app)
    task_routes(app)
