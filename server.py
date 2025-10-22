from http.server import BaseHTTPRequestHandler, HTTPServer
from controllers.user_controller import handle_user_routes
from controllers.task_controller import handle_task_routes
from utils.responses import send_json



class SimpleRequestHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()


    def do_GET(self):
        if self.path.startswith("/tasks"):
            handle_task_routes(self, self.path, "GET")
        else:
            handle_user_routes(self, self.path, "GET")


    def do_POST(self):
        if self.path.startswith("/tasks"):
            handle_task_routes(self, self.path, "POST")
        else:
            handle_user_routes(self, self.path, "POST")   
             

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
    
            


def run(server_class=HTTPServer, handler_class=SimpleRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor corriendo en http://localhost:{port}")
    httpd.serve_forever()

if __name__=="__main__":
    run()