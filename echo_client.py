import socket

for i in range(3):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto("Hi".encode(), ('127.0.0.1', 9999))
    