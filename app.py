from flask import Flask, Blueprint
from flask_cors import CORS
from routes import register_routes
from db_config import connection_pool

# Crear la instancia de Flask
app = Flask(__name__)

# Configurar CORS para permitir peticiones desde Netlify y localhost
CORS(app, resources={r"/api/*": {"origins": [
    "https://todoappacp.netlify.app",
    "http://localhost:4200"
]}}, supports_credentials=True)

# Crear un Blueprint con prefijo /api
api = Blueprint('api', __name__, url_prefix='/api')

# Registrar todas las rutas dentro del Blueprint
register_routes(api)

# Registrar el Blueprint en la app
app.register_blueprint(api)

print("🚀 Servidor Flask inicializado correctamente.")
print("✅ Pool de conexiones creado correctamente. ¡Servidor listo!")

# Punto de entrada
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
