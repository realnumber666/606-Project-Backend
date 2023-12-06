import requests
from http.server import HTTPServer
from routes.transactions import TransactionRoute

ip = "localhost"
port = 8002
service_name = "transaction"

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
    httpd = HTTPServer(server_address, TransactionRoute)

    # start HTTP server
    print(f'Starting transaction service on port {port}...')
    httpd.serve_forever()
else:
    print(f'Failed to connect to registry center.')
    exit()
