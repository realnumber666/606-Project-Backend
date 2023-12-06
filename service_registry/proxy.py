import http.client
import json
from enum import Enum
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse


class ServiceName(Enum):
    USER = 1
    TRANSACTION = 2


name_to_enum = {
    "user": ServiceName.USER,
    "transaction": ServiceName.TRANSACTION
}


path_to_service = {
    '/login': ServiceName.USER,
    '/signup': ServiceName.USER,
    '/expenses': ServiceName.TRANSACTION,
    '/expense': ServiceName.TRANSACTION,
    '/monthly_budget': ServiceName.TRANSACTION,
}

service_to_address = {
    ServiceName.USER: [],
    ServiceName.TRANSACTION: []
}


class ProxyRoute(BaseHTTPRequestHandler):
    def _forward_request(self, method, path, data=None):
        # Open a connection to the microservice
        if method == "GET":
            parsed_path = urlparse(self.path)
            mapping_path = parsed_path.path
        elif method == "PUT":
            mapping_path = f"/{self.path.split('/')[1]}"
        else:
            mapping_path = path
        service = path_to_service[mapping_path]
        service_host = service_to_address[service][0]
        service_port = service_to_address[service][1]
        connection = http.client.HTTPConnection(service_host, service_port)

        body = json.dumps(data) if data is not None else None
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

        if self.path == '/services/register':
            status, response_data = self.register_service(data)
        else:
            # Forward the request to the microservice and get the response
            status, response_data = self._forward_request(method, self.path, data)

        # Send the response back to the client
        self._send_response(status, response_data)

    def do_GET(self):
        status, response_data = self._forward_request('GET', self.path)
        self._send_response(status, response_data)

    def do_DELETE(self):
        content_length = int(self.headers.get('Content-Length', 0))
        request_body = self.rfile.read(content_length) if content_length > 0 else '{}'
        data = json.loads(request_body.decode('utf-8'))

        status, response_data = self._forward_request('DELETE', self.path, data)
        self._send_response(status, response_data)

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        request_body = self.rfile.read(content_length)
        data = json.loads(request_body.decode('utf-8'))

        status, response_data = self._forward_request('PUT', self.path, data)
        self._send_response(status, response_data)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def register_service(self, data):
        serviceName = data.get("serviceName")
        ip = data.get("ip")
        port = data.get("port")

        service_to_address[name_to_enum[serviceName]] = [ip, int(port)]

        status, response_data = 200, {}

        return status, response_data
