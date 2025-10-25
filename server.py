import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from controllers.user_controller import handle_user_routes
from controllers.task_controller import handle_task_routes
from utils.responses import send_json

# --- CLASE HANDLER CORREGIDA ---
class SimpleRequestHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        # Manejo de CORS PRE-FLIGHT (OPTIONS)
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "https://todoappacp.netlify.app")
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()


    def do_GET(self):
        # Manejo de la RUTA RAÍZ para verificar que el servidor esté vivo
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "https://todoappacp.netlify.app")
            self.end_headers()
            # Mensaje simple de estado para verificar el deploy
            self.wfile.write(b'{"status": "API is operational"}') 
        
        elif self.path.startswith("/tasks"):
            handle_task_routes(self, self.path, "GET")
        
        else:
            # Asume que cualquier otra ruta GET es para user_controller (ej. /users)
            handle_user_routes(self, self.path, "GET")


    def do_POST(self):
        if self.path.startswith("/tasks"):
            handle_task_routes(self, self.path, "POST")
        else:
            handle_user_routes(self, self.path, "POST")
            
    # Los métodos do_PUT y do_DELETE están bien si solo manejan /tasks y /users
    def do_PUT(self):
        if self.path.startswith("/tasks"):
            handle_task_routes(self, self.path, "PUT")
        else:
            handle_user_routes(self, self.path, "PUT")

    def do_DELETE(self):
        if self.path.startswith("/tasks"):
            handle_task_routes(self, self.path, "DELETE")
        else:
            handle_user_routes(self, self.path, "DELETE")


# --- FUNCIÓN DE EJECUCIÓN CORREGIDA ---
def run(server_class=HTTPServer, handler_class=SimpleRequestHandler):
    # ✅ RENDER: Obtiene el puerto dinámico. Es CRUCIAL que el host sea '0.0.0.0'
    port = int(os.environ.get("PORT", 8000))
    # '0.0.0.0' asegura que el servidor escuche en todas las interfaces de red, 
    # lo cual es necesario en entornos de contenedores como Render.
    server_address = ('0.0.0.0', port) 
    
    try:
        httpd = server_class(server_address, handler_class)
        print(f"✅ Servidor corriendo en http://0.0.0.0:{port}")
        httpd.serve_forever()
    except Exception as e:
        print(f"❌ Error al iniciar el servidor: {e}")

if __name__=="__main__":
    run()