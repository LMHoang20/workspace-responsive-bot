from http.server import BaseHTTPRequestHandler, HTTPServer

import base64
import json

class SubscriberPush:
    def __init__(self, subscription_id) -> None:
        self.subscription_id = subscription_id
        pass
        
    def start(self, callback):
        class Receiver(BaseHTTPRequestHandler):
            def do_POST(req):
                try:
                    message = CustomRequest(req)
                    assert message.subscription_id == self.subscription_id, \
                        f'Invalid subscription id: {message.subscription_id} != {self.subscription_id}'
                except Exception as e:
                    print(f'Error: {e}')
                    CustomRequest._nack(req)
                    return
                callback(message)

        def run_server(server_class=HTTPServer, handler_class=Receiver, port=8080):
            server_address = ('', port)
            httpd = server_class(server_address, handler_class)
            print('Starting https...')
            httpd.serve_forever()

        run_server()

class CustomRequest:
    def __init__(self, request) -> None:
        self.request = request
        body = json.loads(request.rfile.read(int(request.headers['Content-Length'])).decode())
        self.data = base64.b64decode(body['message']['data'])
        self.subscription_id = body['subscription'].split('/')[-1]
    
    def ack(self):
        CustomRequest._ack(self.request)

    def nack(self):
        CustomRequest._nack(self.request)

    @staticmethod
    def _ack(req):
        req.send_response(200)
        req.end_headers()
        req.wfile.write(json.dumps({'status': 'success'}).encode())

    @staticmethod
    def _nack(req):
        req.send_response(400)
        req.end_headers()
        req.wfile.write(json.dumps({'status': 'error'}).encode())