import http.client
import json
from enum import Enum
from http.server import HTTPServer, BaseHTTPRequestHandler

USER_SERVICE_HOST = 'localhost'
USER_SERVICE_PORT = 8001

TRANSACTION_SERVICE_HOST = 'localhost'
TRANSACTION_SERVICE_PORT = 8001


class ServiceName(Enum):
    USER = 1
    TRANSACTION = 2


path_to_service = {
    '/login': ServiceName.USER,
    '/signup': ServiceName.USER,
    '/expenses': ServiceName.TRANSACTION,
    '/monthly_budget': ServiceName.TRANSACTION,
}

service_to_address = {
    ServiceName.USER: [USER_SERVICE_HOST, USER_SERVICE_PORT],
    ServiceName.TRANSACTION: [TRANSACTION_SERVICE_HOST, TRANSACTION_SERVICE_PORT]
}


class ProxyRoute(BaseHTTPRequestHandler):
    def _forward_request(self, method, path, data):
        # Open a connection to the microservice
        service = path_to_service[path]
        service_host = service_to_address[service][0]
        service_port = service_to_address[service][1]
        connection = http.client.HTTPConnection(service_host, service_port)

        # Prepare headers
        headers = {'Content-type': 'application/json'}

        # Send the request to the microservice
        print(f"Proxy a request <{method}> <{path}> <{data}>")
        connection.request(method, path, body=json.dumps(data), headers=headers)

        # Get the response from the microservice
        response = connection.getresponse()
        response_data = response.read().decode()
        connection.close()

        # Return the status code and the data
        return response.status, response_data

    def _send_response(self, status, data=None):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        if data:
            self.wfile.write(data.encode('utf-8'))

    def do_POST(self):
        method = 'POST'
        content_length = int(self.headers['Content-Length'])
        request_body = self.rfile.read(content_length)
        data = json.loads(request_body.decode('utf-8'))

        # Forward the request to the microservice and get the response
        status, response_data = self._forward_request(method, self.path, data)

        # Send the response back to the client
        self._send_response(status, response_data)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
