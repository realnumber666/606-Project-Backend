from http.server import HTTPServer
from routes.transactions import TransactionRoute

# create server and set port
server_address = ('', 8000)
httpd = HTTPServer(server_address, TransactionRoute)

# start HTTP server
print('Starting server on port 8000...')
httpd.serve_forever()
