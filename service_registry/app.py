from http.server import HTTPServer
from proxy import ProxyRoute

port = 8000
# create server and set port
server_address = ('', port)
httpd = HTTPServer(server_address, ProxyRoute)

# start HTTP server
print(f'Starting service registry on port {port}...')
httpd.serve_forever()
