import socket
import threading
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def keep_listening(conn, decryptor):
    while True:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = decryptor.update(data) + decryptor.finalize()
            data = data[:len(data)//16]
            print("Received:", data.decode())
        time.sleep(0.1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    r = s.recv(1024)
    key = r[:32]
    iv = r[32:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    decryptor = cipher.decryptor()

    t = threading.Thread(target=keep_listening, args=(s,decryptor))
    t.start()

    while True:
        data = input("")
        data = (data*16).encode()
        data = encryptor.update(data) + encryptor.finalize()
        s.sendall(data)