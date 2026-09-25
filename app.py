"""Order service for a deliberately vulnerable, localhost-only test fixture."""
import argparse
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit


ORDERS = [
    {'id': 1001, 'customer_id': 'alice', 'item': 'Demo keyboard', 'total': 45,
     'shipping_address': '12 Example Street, Mock City'},
    {'id': 1002, 'customer_id': 'bob', 'item': 'Demo headphones', 'total': 80,
     'shipping_address': '34 Fictional Avenue, Mock City'},
    {'id': 1003, 'customer_id': 'alice', 'item': 'Demo mouse', 'total': 20,
     'shipping_address': '12 Example Street, Mock City'},
]


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, value):
        body = json.dumps(value).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        customer = self.headers.get('X-Customer-ID')
        if customer not in {'alice', 'bob'}:
            return self.send_json(401, {'error': 'Customer context required'})
        path = urlsplit(self.path).path
        if path == '/orders':
            return self.send_json(200, {'orders': [o for o in ORDERS if o['customer_id'] == customer]})
        match = re.fullmatch(r'/orders/([0-9]+)', path)
        if match:
            order = next((o for o in ORDERS if o['id'] == int(match[1])), None)
            if order is None:
                return self.send_json(404, {'error': 'Order not found'})
            return self.send_json(200, order)
        self.send_json(404, {'error': 'Route not found'})


def make_server(port=8766):
    return ThreadingHTTPServer(('127.0.0.1', port), Handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8766)
    args = parser.parse_args()
    server = make_server(args.port)
    print(f'Orders API: http://127.0.0.1:{server.server_port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
