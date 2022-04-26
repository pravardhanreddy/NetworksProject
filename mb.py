import socket

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.connect(('127.0.0.1', 9090))

for i in range(2):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto("Hi".encode(), ('127.0.0.1', 9999))

port = int(tcp_sock.recv(1024).decode())
tcp_sock.close()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto("Hi".encode(), ('172.0.0.1', port))

