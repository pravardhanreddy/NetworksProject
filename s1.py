import socket

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind(('0.0.0.0', 9090))
tcp_sock.listen()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 9999))

l = []

# Client1

conn1, client1 = tcp_sock.accept()

for i in range(2):
    msg, add = s.recvfrom(1024)
    l.append(add[1])
    print(add[1])
prediction1 = 2 * l[1] - l[0]
print('prediction1:', prediction1)

# msg, add = s.recvfrom(1024)
# print(add[1])

# if prediction == add[1]:
#     print("Success")
# else:
#     print("Fail. Predicted:", prediction)

# Client2

conn2, client2 = tcp_sock.accept()

for i in range(2):
    msg, add = s.recvfrom(1024)
    l.append(add[1])
    print(add[1])
prediction2 = 2 * l[3] - l[2]
print('prediction2:', prediction2)

# msg, add = s.recvfrom(1024)
# print(add[1])

# if prediction == add[1]:
#     print("Success")
# else:
#     print("Fail. Predicted:", prediction)

conn2.sendall(str(prediction1).encode())
conn1.sendall(str(prediction2).encode())

tcp_sock.close()