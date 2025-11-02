import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from routes import handle_request

# Crear la instancia de Flask
app = Flask(__name__)

# Configurar CORS (permite solicitudes desde tu frontend en Netlify)
CORS(app, resources={r"/api/*": {"origins": ["https://todoappacp.netlify.app", "http://localhost:4200"]}})

# Ruta general que maneja todos los endpoints /api/*
@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def api_router(path):
    # Si el navegador envía una solicitud OPTIONS (CORS preflight), responder de inmediato
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return response, 200

    method = request.method
    body = request.get_json(silent=True)
    full_path = f"/{path}"

    try:
        # Llamar al manejador principal de rutas
        response_data = handle_request(
            path=full_path,
            method=method,
            body=body,
            query_params=request.args.to_dict()
        )

        # Extraer código de estado (por defecto 200)
        status_code = response_data.pop('status', 200)

        # Si hay error pero el código es <400, corregirlo
        if 'error' in response_data and status_code < 400:
            status_code = 400

        return jsonify(response_data), status_code

    except Exception as e:
        # Manejo de errores no controlados
        print(f"❌ Error en api_router: {e}")
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500


# Punto de entrada para ejecución directa
if __name__ == '__main__':
    # Modo desarrollo local (no usar en producción)
    app.run(host='0.0.0.0', port=8000, debug=True)
