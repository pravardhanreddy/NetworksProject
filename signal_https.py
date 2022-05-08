import socket
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


HOST = "0.0.0.0"  # Bind to all IPs
PORT = 8443  # Port to listen on (non-privileged ports are > 1023)    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    peers = []

    while True:
        conn1, addr1 = s.accept()
        conn1.sendall(b'Waiting for the other peer') # Send to the first peer that connects

        conn2, addr2 = s.accept()
        conn2.sendall(b'Both peers connected. Generating and sending keys and IP now') # Send to the second peer
        
        key = ChaCha20Poly1305.generate_key()
        nonce = os.urandom(12)
        aad = b"This project is really cool"

        print('sending keys to peer1')
        conn1.sendall(key+nonce+aad + addr2[0].encode()) # Key and IP Information

        print('sending keys to peer2')
        conn2.sendall(key+nonce+aad + addr1[0].encode())
