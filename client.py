import socket
import threading
import time
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

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
    s.connect((HOST, PORT))

    r = s.recv(1024)
    key = r[:32]
    nonce = r[32:44]
    aad = r[44:]
    chacha = ChaCha20Poly1305(key)

    t = threading.Thread(target=keep_listening, args=(s,chacha))
    t.start()

    while True:
        data = input("")
        data = data.encode()
        data = chacha.encrypt(nonce, data, aad)
        s.sendall(data)