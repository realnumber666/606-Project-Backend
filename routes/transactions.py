import json
from http.server import BaseHTTPRequestHandler
from controllers.transactions import TransactionController


class TransactionRoute(BaseHTTPRequestHandler):
    def _send_response(self, status, data=None):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        # 添加CORS头部，允许来自所有域的请求
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

        self.end_headers()
        if data:
            self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        if self.path == '/expenses':
            response = TransactionController.get_expenses()
            self._send_response(200, response)
        else:
            self._send_response(404, {'error': 'Not Found'})

    def do_POST(self):
        if self.path == '/expenses':
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            data = json.loads(request_body.decode('utf-8'))

            record_id = data.get('record_id')
            amount = data.get('amount')
            description = data.get('description', '')
            datetime = data.get('datetime')
            category = data.get('category')

            response = TransactionController.add_expense(record_id, amount, description, datetime, category)

            self._send_response(200, response)
        else:
            self._send_response(404, {'error': 'Not Found'})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')  # 允许所有域访问，可以根据需求设置
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')  # 允许的HTTP方法
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')  # 允许的请求头
        self.end_headers()
