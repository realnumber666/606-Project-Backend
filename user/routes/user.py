import json
from http.server import BaseHTTPRequestHandler
from user.controllers.user import UserController


class UserRoute(BaseHTTPRequestHandler):
    def _send_response(self, status, data=None):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')

        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

        self.end_headers()
        if data:
            self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            data = json.loads(request_body.decode('utf-8'))

            username = data.get('username')
            password = data.get('password')

            response = UserController.login(username, password)
            self._send_response(response['status'], response)

        elif self.path == '/signup':
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            data = json.loads(request_body.decode('utf-8'))

            username = data.get('username')
            password = data.get('password')
            fullName = data.get('fullName')

            response = UserController.signup(username, password, fullName)
            self._send_response(response['status'], response)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
