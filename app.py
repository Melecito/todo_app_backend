import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from routes import handle_request

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "https://todoappacp.netlify.app/"}})

@app.route('/api/<path:path>', method=['GET', 'POST', 'PUT', 'DELETE'])
def api_router(path):
    method = request.method
    body = request.get_json(silent=True)

    full_path = f"/{path}"

    response_data = handle_request(
        path=full_path,
        method=method,
        body=body,
        query_params=request.args.to_dict()
    )

    status_code = response_data.pop('status', 200)

    if 'error' in response_data and status_code < 400:
        status_code = 400

    return jsonify(response_data), status_code