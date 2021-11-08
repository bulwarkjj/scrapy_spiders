import socket

target_host = "127.0.0.1" # standard IVANA ip address for loopback, enables server/client processes on a single system
target_port = 9998

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# ref tcp_client.py for socket.AF_INET and socket.SOCK_DGRAM explanation
# since UDP is a connectionless protocol, no need to call connect() like in tcp_client.py

# send some data
client.sendto(b"AAAAAAGGGHHH monsters", (target_host, target_port))

# receive some data
data, addr = client.recvfrom(4096)

print(data.decode())
client.close()