import socket
import threading
import time
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

HOST = "103.228.33.114"  # The server's hostname or IP address
PORT = 8443  # The port used by the server
SRC_PORT  = 50002
PEER_PORT = 50001


def keep_listening(listener, chacha):
    while True:
        while True:
            data, _ = listener.recvfrom(1024)
            if not data:
                break
            data = chacha.decrypt(nonce, data, aad)
            print("Received:", data.decode())
        time.sleep(0.1)


# Signalling Server Communication
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    r = s.recv(1024) # Connect and get first message
    print(r.decode())
    print('Waiting to receive Keys')
    r = s.recv(1024) # receive the keys
    key = r[:32]
    nonce = r[32:44]
    aad = r[44:71]
    chacha = ChaCha20Poly1305(key)
    PEER_IP = r[71:].decode()
    print('Keys received, waiting for IP')
    print(PEER_IP)
    s.close()

# Punch a hole
listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listener.bind(('0.0.0.0', PEER_PORT))
listener.sendto(b'Punch Hole', (PEER_IP, SRC_PORT))

# Send data through the punched hole
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender.bind(('0.0.0.0', SRC_PORT))

t = threading.Thread(target=keep_listening, args=(listener,chacha))
t.start()

while True:
    data = input("")
    data = data.encode()
    data = chacha.encrypt(nonce, data, aad)
    sender.sendto(data, (PEER_IP, PEER_PORT))
