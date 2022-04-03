import socket
import threading
import time
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

aad = b"authenticated but unencrypted data"
key = ChaCha20Poly1305.generate_key()
chacha = ChaCha20Poly1305(key)
nonce = os.urandom(12)

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

def keep_listening(conn, chacha):
    while True:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = chacha.decrypt(nonce, data, aad)
            print("Received:", data.decode())
        time.sleep(0.1)
    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    conn.sendall(key+nonce+aad)

    t = threading.Thread(target=keep_listening, args=(conn,chacha))
    t.start()

    with conn:
        print(f"Connected by {addr}")
        while True:
            data = input("")
            data = data.encode()
            data = chacha.encrypt(nonce, data, aad)
            conn.sendall(data)