from flask import Flask
from flask_cors import CORS
from routes import register_routes
from db_config import connection_pool

# Crear la instancia de Flask
app = Flask(__name__)

# Configurar CORS
CORS(app, resources={r"/api/*": {"origins": ["https://todoappacp.netlify.app", "http://localhost:4200"]}}, supports_credentials=True)


# Registrar rutas desde routes.py
register_routes(app)

print("🚀 Servidor Flask inicializado correctamente.")
print("✅ Pool de conexiones creado correctamente. ¡Servidor listo!")

# Punto de entrada
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)

