import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 9999))
# s.listen()

l = []

for i in range(2):
    msg, add = s.recvfrom(1024)
    l.append(add[1])
    print(add[1])
prediction = 2 * l[1] - l[0]

msg, add = s.recvfrom(1024)
print(add[1])

if prediction == add[1]:
    print("Success")
else:
    print("Fail")

# s.close()