import json
from http.server import BaseHTTPRequestHandler
from transaction.controllers.transactions import TransactionController
from urllib.parse import urlparse, parse_qs


class TransactionRoute(BaseHTTPRequestHandler):
    def _send_response(self, status, data=None):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')

        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

        self.end_headers()
        if data:
            self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/expenses':
            # API Get monthly expenses
            query_params = parse_qs(parsed_path.query)
            month = query_params.get('month', [None])[0]
            user = query_params.get('user', [None])[0]

            if month:
                year, month = month.split('-')
                response = TransactionController.get_expenses(year, month, user)
            else:
                response = TransactionController.get_expenses()

            self._send_response(200, response)
        elif parsed_path.path == '/monthly_budget':
            # API Get monthly budget
            query_params = parse_qs(parsed_path.query)
            month = query_params.get('month', [None])[0]
            username = query_params.get('user', [None])[0]

            year, month = month.split('-')
            response = TransactionController.get_monthly_budget(year, month, username)

            self._send_response(200, response)
        
        else:
            self._send_response(404, {'error': 'Not Found'})

    def do_DELETE(self):
        if self.path == '/expense':
            # API Delete one expenses
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            data = json.loads(request_body.decode('utf-8'))

            record_id = data.get('id')
            response = TransactionController.delete_expense(record_id)
            self._send_response(200, response)
        else:
            self._send_response(404, {'error': 'Not Found'})

    def do_POST(self):
        if self.path == '/expenses':
            # API Add one expense
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            data = json.loads(request_body.decode('utf-8'))

            amount = data.get('amount')
            description = data.get('description', '')
            datetime = data.get('datetime')
            category = data.get('category')
            username = data.get('username')

            response = TransactionController.add_expense(amount, description, datetime, category, username)

            self._send_response(200, response)
        elif self.path == '/monthly_budget':
            # API Update monthly budget
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            data = json.loads(request_body.decode('utf-8'))

            username = data.get('User')
            year = data.get('Year')
            month = data.get('Month')
            totalAmount = data.get('TotalAmount')
            response = TransactionController.set_monthly_budget(username, year, month, totalAmount)

            self._send_response(200, response)
        else:
            self._send_response(404, {'error': 'Not Found'})

    def do_PUT(self):
        if self.path.startswith('/expenses'):
            # API Update one expenses
            expenseId = self.path.split('/')[-1]

            # Read the request body
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            data = json.loads(request_body.decode('utf-8'))

            # Extract the necessary information from the data
            amount = data.get('amount')
            description = data.get('description', '')  # Default to empty string if not provided
            datetime = data.get('datetime')
            category = data.get('category')

            response = TransactionController.update_expense(expenseId, amount, description, datetime, category)

            self._send_response(200, response)

        else:
            self._send_response(404, {'error': 'Not Found'})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        





