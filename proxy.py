import socket
from _thread import *

from command_handler_proxy_server import ClientCommandHandler
from consts import EXIT_MESSAGE, HOST, PORT_P_PROXY_SEREVR, PORT_P_MAIN_SERVER

def client_handler(client_connection, server_socket):
    client_connection.send(str.encode(f'Connected to the proxy server.'))
    cmd_handler = ClientCommandHandler()
    while True:
        data = client_connection.recv(2048)
        message = data.decode('utf-8')
        print("message:", message)
        if message == EXIT_MESSAGE:
            client_connection.sendall(str.encode(EXIT_MESSAGE))
            break
        reply, forward = cmd_handler.onecmd(message) or ("invalid command", False)
        print("reply:", reply, "forward:", forward)
        if forward:
            server_socket.send(str.encode(message + " " + reply))  # "message username" 
            reply = server_socket.recv(1024).decode('utf-8')
        client_connection.sendall(str.encode(reply))
    client_connection.close()

def accept_connections(client_socket, server_socket):
    client, address = client_socket.accept()
    print(f'Connected to: {address[0]}:{str(address[1])}')
    start_new_thread(client_handler, (client, server_socket))

client_socket = socket.socket()
server_socket = socket.socket()
try:
    client_socket.bind((HOST, PORT_P_PROXY_SEREVR))
except socket.error as e:
    print(f"An error occured {str(e)}")

try:
    server_socket.connect((HOST, PORT_P_MAIN_SERVER))
except socket.error as e:
    print(f"An error occurred {str(e)}")
    exit()

print(f'Proxy server is listing on the port {PORT_P_PROXY_SEREVR}...')
client_socket.listen()

while True:
    accept_connections(client_socket, server_socket)
