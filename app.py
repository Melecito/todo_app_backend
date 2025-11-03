from flask import Flask
from flask_cors import CORS
from controllers.user_controller import user_bp
from controllers.task_controller import task_bp

# Crear la instancia principal de Flask
app = Flask(__name__)

# Configurar CORS (permite peticiones desde tu frontend)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://todoappacp.netlify.app",  # dominio de tu frontend en producción
            "http://localhost:4200"             # para desarrollo local
        ]
    }
})

# Registrar los blueprints
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(task_bp, url_prefix="/api")

# Mensaje de inicio del servidor
@app.before_first_request
def startup_message():
    print("✅ Servidor Flask iniciado correctamente y listo para recibir peticiones...")

# Punto de entrada
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
