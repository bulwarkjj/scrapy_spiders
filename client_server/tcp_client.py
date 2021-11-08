import socket

target_host = 'www.google.com' # if host is an empty string server will accept connections on all available IPv4 interfaces
target_port = 80

#  create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.AF_INET = indicates using a standard IP4 address
# socket.SOCK_STREAM = indicates using asocket type for TCP (protcol used to transmit my messages in the network)

# connect the client
client.connect((target_host, target_port))

# send some data
client.send(b"GET / HTTP/1.1\r\nHOST: google.com\r\n\r\n")

# recieve some data
response = client.recv(4096)
# 4096 = bit limit 

print(response.decode())
client.close

"""
Possible better way to write this, this is short and closes by itself, but not as readable as the above code

HOST = 'www.google.com'
PORT = 1068 # unprivileged ports are > 1023 so this may work better 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    client.connect((target_host, target_port))
    client.send(b"GET / HTTP/1.1\r\nHOST: google.com\r\n\r\n")
    response = client.recv(4096)
 
"""