import socket
import threading
import time
import pickle
import signal
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

def handler(signum, frame):
    res = input("\nCtrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)
 
signal.signal(signal.SIGINT, handler)


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 9000  # The port used by the server
PEER_ID = "client2"
PEER_PORT = 9001

def keep_listening(conn, chacha):
    while True:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = chacha.decrypt(nonce, data, aad)
            if data == "exit":
                conn.close()
                return
            print("Received:", data.decode())
        time.sleep(0.1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    id = (PEER_ID, PEER_PORT)
    s.sendall(pickle.dumps(id))
    data = s.recv(1024)
    peers_dict = pickle.loads(data)

    print(peers_dict)
    i = input('Select which peer to connect to (if receiving connections enter r):')
    s.sendall(i.encode())
    if i == 'r' or i in peers_dict:
        r = s.recv(1024)
        key = r[:32]
        nonce = r[32:44]
        aad = r[44:]
        chacha = ChaCha20Poly1305(key)

        s.close()

        if i != 'r':
            peer_host, peer_port = peers_dict[i]
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((peer_host, peer_port)) 

        if i == 'r':
            p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            p.bind(('0.0.0.0', PEER_PORT))
            p.listen()
            s, addr = p.accept()
        t = threading.Thread(target=keep_listening, args=(s,chacha))
        t.start()

        while True:
            data = input("")
 
            data = data.encode()
            data = chacha.encrypt(nonce, data, aad)
            s.sendall(data)
            if data == "exit":
                s.close()
                p.close()
                break