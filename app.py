from flask import Flask
from flask_cors import CORS
from routes import register_routes
from db_config import connection_pool

app = Flask(__name__)

# ✅ Configurar CORS de forma global
CORS(app, resources={r"/*": {
    "origins": [
        "https://todoappacp.netlify.app",
        "https://unattaining-enrico-elastically.ngrok-free.dev"
    ],
    "supports_credentials": True,
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# ✅ Registrar las rutas después de habilitar CORS
register_routes(app)

print("🚀 Servidor Flask inicializado correctamente.")
print("✅ Pool de conexiones creado correctamente. ¡Servidor listo!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
