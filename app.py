from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes import register_routes
from db_config import connection_pool

# Crear la instancia de Flask
app = Flask(__name__)

# Configurar CORS para Netlify y localhost
CORS(app, resources={r"/api/*": {"origins": [
    "https://todoappacp.netlify.app",
    "http://localhost:4200"
]}}, supports_credentials=True)

# 🔐 Configuración de JWT
app.config["JWT_SECRET_KEY"] = "clave_super_secreta_123"  # cambia esto por una clave segura
app.config["JWT_TOKEN_LOCATION"] = ["headers"]  # <- esta línea evita el KeyError
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"

# Inicializar JWT
jwt = JWTManager(app)

# Registrar rutas desde routes.py (ya incluye /api)
register_routes(app)

print("🚀 Servidor Flask inicializado correctamente.")
print("✅ Pool de conexiones creado correctamente. ¡Servidor listo!")

# Punto de entrada
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=False)
