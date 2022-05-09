import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from http.server import BaseHTTPRequestHandler, HTTPServer


HOST = "0.0.0.0"  # Bind to all IPs
PORT = 50000  # Port to listen on (non-privileged ports are > 1023)


class handler(BaseHTTPRequestHandler):
    # Checks if the connecting peer is peer 1.
    # Will be set to False after peer 1 has connected.
    # Will be reset to True after peer 2 has connected.
    first_peer = True

    peers = {}
    key = ChaCha20Poly1305.generate_key()
    nonce = os.urandom(12)
    aad = b"This project is really cool"

    def log_message(self, format, *args):
        return

    def send_keys(self):
        if handler.first_peer:  # If peer 1 is connecting then generate new keys
            print('Generating new keys...')
            handler.key = ChaCha20Poly1305.generate_key()
            handler.nonce = os.urandom(12)
        self.wfile.write(handler.key + handler.nonce + handler.aad)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if self.path == '/register':
            self.send_keys()
            if handler.first_peer:
                self.peers[1] = self.headers['X-Forwarded-For']  # Peer 1
                print('Sending Keys to peer 1:', self.peers[1])
            else:
                self.peers[2] = self.headers['X-Forwarded-For']  # Peer 2
                print('Sending keys to peer 2:', self.peers[2])
            handler.first_peer = not handler.first_peer

        elif self.path == '/connect':
            if not handler.first_peer: # This means peer2 has not registered yet
                self.wfile.write(b'wait')
                # print('Asking peer 1 to wait for peer 2')
            elif self.peers[1] == self.headers['X-Forwarded-For']: # Reguest from peer 1
                # So send address of peer 2
                self.wfile.write(self.peers[2].encode())
            else: # Request from peer 2
                # So send address of peer 1
                self.wfile.write(self.peers[1].encode())

        else:
            self.wfile.write(b'Invalid Request')
            

with HTTPServer((HOST, PORT), handler) as server:
    server.serve_forever()
