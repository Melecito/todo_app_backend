from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes import register_routes
from db_config import connection_pool
import os

# Crear la instancia de Flask
app = Flask(__name__)

# Configurar CORS para Netlify y localhost
# Configurar CORS
# ✅ Configurar CORS correctamente
CORS(app, resources={r"/api/*": {"origins": [
    "https://todoappacp.netlify.app",
    "http://localhost:4200"
]}}, 
supports_credentials=True,
allow_headers=["Content-Type", "Authorization"],
expose_headers=["Authorization"])  # 👈 ESTA LÍNEA ES CLAVE



# 🔐 Configuración de JWT
# 🔧 Permitir explícitamente que Angular envíe Authorization en CORS
app.config["CORS_HEADERS"] = "Content-Type, Authorization"
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")  # cambia esto por una clave segura
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
    app.run(host='0.0.0.0', port=8000, debug=False)
