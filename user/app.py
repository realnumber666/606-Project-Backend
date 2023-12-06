import requests
from http.server import HTTPServer
from routes.user import UserRoute

ip = "localhost"
port = 8001
service_name = "user"

url = 'http://localhost:8000/services/register'

data = {
    'serviceName': service_name,
    'ip': ip,
    'port': port
}

response = requests.post(url, json=data)

if response.status_code == 200:
    # create server and set port
    server_address = ('', port)
    httpd = HTTPServer(server_address, UserRoute)

    # start HTTP server
    print(f'Starting user service on port {port}...')
    httpd.serve_forever()
else:
    print(f'Failed to connect to registry center.')
    exit()
