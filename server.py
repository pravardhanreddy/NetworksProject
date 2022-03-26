import socket
import threading
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

def keep_listening(conn, addr):
    while True:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("Received:", data.decode())
        time.sleep(0.1)
    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    t = threading.Thread(target=keep_listening, args=(conn,addr))
    t.start()

    with conn:
        print(f"Connected by {addr}")
        while True:
            data = input("")
            conn.sendall(data.encode())