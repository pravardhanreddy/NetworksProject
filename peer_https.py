import requests
import time
import socket
import threading
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


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


response = requests.get('https://signal.pravardhan-reddy5-1.tk/register')
r = response.content
key = r[:32]
nonce = r[32:44]
aad = r[44:]
chacha = ChaCha20Poly1305(key)
print('key:', key)
print('nonce:', nonce)
print('aad:', aad)

PEER_IP = ''
while True:
    response = requests.get('https://signal.pravardhan-reddy5-1.tk/connect')
    if response.content == b'wait':
        print('waiting...')
        time.sleep(2)
    else:
        PEER_IP = response.content.decode()
        break

print(PEER_IP)

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