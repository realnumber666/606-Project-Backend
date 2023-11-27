from http.server import HTTPServer
from routes.user import UserRoute

port = 8001
# create server and set port
server_address = ('', port)
httpd = HTTPServer(server_address, UserRoute)

# start HTTP server
print(f'Starting user service on port {port}...')
httpd.serve_forever()
