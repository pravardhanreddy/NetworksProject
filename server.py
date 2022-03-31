import socket
import threading
import time
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Encryption 
key = os.urandom(32)
iv = os.urandom(16)
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
encryptor = cipher.encryptor()

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

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
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    conn.sendall(key+iv)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    decryptor = cipher.decryptor()

    t = threading.Thread(target=keep_listening, args=(conn,decryptor))
    t.start()

    with conn:
        print(f"Connected by {addr}")
        while True:
            data = input("")
            data = (data*16).encode()
            data = encryptor.update(data) + encryptor.finalize()
            conn.sendall(data)