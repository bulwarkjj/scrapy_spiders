import socket
import threading

IP = "0.0.0.0"
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)
    # listen(5) sets the maximum back-log of connections
    print(f"[*] Listening on {IP}:{PORT}")

    # Loop to start listening for incoming traffic
    while True:
        client, address = server.accept()  # catches when a client connects
        # client receives the client socket
        # address receives the remote connection details
        print(f"[*] Accepted connection from {address[0]}:{address[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()  # starts new thread object that points to handle_client()
        # This threading allows for one thread to be applied to each connection and allowing another thread to wait for next connection
      

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f"[*] Recieved: {request.decode('UTF-8')}")
        sock.send(b'ACK')

if __name__ == '__main__':
    main()