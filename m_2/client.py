# Client
import socket

address = 'localhost'
port = 8000


def socket_client_connection(address, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((address, port))


def socket_client_send_receive(address, port):
    con = socket_client_connection(address, port)

    con.send("Hello from Client".encode())

    data = con.recv(1024).decode()
    print(f"Received: {data}")

    client_socket.close()
