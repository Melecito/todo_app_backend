from flask import Blueprint
from controllers.user_controller import user_bp
from controllers.task_controller import task_bp

def register_routes(app):
    # Prefijo común /api
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(task_bp, url_prefix="/api")
