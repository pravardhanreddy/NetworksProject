import socket
import threading
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def keep_listening(conn, addr):
    while True:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("Received:", data.decode())
        time.sleep(0.1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    t = threading.Thread(target=keep_listening, args=(s,""))
    t.start()

    while True:
        data = input("")
        s.sendall(data.encode())