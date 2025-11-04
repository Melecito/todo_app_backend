from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from routes import register_routes
from db_config import connection_pool

app = Flask(__name__)

# Configuración de CORS (Netlify, localhost y ngrok)
CORS(app, resources={r"/api/*": {"origins": [
    "https://todoappacp.netlify.app",
    "http://localhost:4200",
    "https://*.ngrok-free.app",
    "https://*.ngrok-free.dev"
]}}, supports_credentials=True)

# Crear un blueprint con prefijo /api
api = Blueprint('api', __name__, url_prefix='/api')

# Registrar rutas desde routes.py
register_routes(api)

# Endpoint raíz para verificar que el servidor responde
@api.route('/', methods=['GET'])
def index():
    return jsonify({"status": "ok", "message": "API corriendo correctamente"})

# Registrar el blueprint
app.register_blueprint(api)

print("🚀 Servidor Flask inicializado correctamente.")
print("✅ Pool de conexiones creado correctamente. ¡Servidor listo!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
