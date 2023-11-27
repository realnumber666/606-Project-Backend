from http.server import HTTPServer
from routes.transactions import TransactionRoute

port = 8002
# create server and set port
server_address = ('', port)
httpd = HTTPServer(server_address, TransactionRoute)

# start HTTP server
print(f'Starting transaction service on port {port}...')
httpd.serve_forever()
