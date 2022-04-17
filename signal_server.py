import socket
import threading
import time
import os
import signal
import pickle
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

def handler(signum, frame):
    res = input("\nCtrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)
 
signal.signal(signal.SIGINT, handler)

aad = b"This project is really cool"
key = ChaCha20Poly1305.generate_key()
chacha = ChaCha20Poly1305(key)
nonce = os.urandom(12)

HOST = "0.0.0.0"  # Bind to all IPs
PORT = 9000  # Port to listen on (non-privileged ports are > 1023)

def keep_listening(conn, chacha):
    while True:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = chacha.decrypt(nonce, data, aad)
            print("Received:", data.decode())
        time.sleep(0.1)

peers_dict = {}
def handle_connection(conn, addr):

    global peers_dict

    data = conn.recv(1024) # recv id and port from the peer
    id = pickle.loads(data)
    peers_dict[id[0]] = (addr[0], id[1])
    print(peers_dict)
    conn.sendall(pickle.dumps(peers_dict))
    data = conn.recv(1024) # user input from peer
    data = data.decode()
    if data == 'r' or data in peers_dict:
        conn.sendall(key+nonce+aad)
        conn.close()
    else:
        print("Invalid input received, exiting")

    # t = threading.Thread(target=keep_listening, args=(conn,chacha))
    # t.start()

    # with conn:
    #     print(f"Connected by {addr}")
    #     while True:
    #         data = input("")
    #         data = data.encode()
    #         data = chacha.encrypt(nonce, data, aad)
    #         conn.sendall(data)
    conn.close()
    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_connection, args=(conn,addr))
        t.start()

