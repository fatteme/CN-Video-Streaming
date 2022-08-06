import socket
from _thread import *

from command_handler_main_server import ClientCommandHandler
from command_handler_main_server import ProxyCommandHandler
from constraints import EXIT_MESSAGE, HOST, PORT, PORT_P_MAIN_SERVER

def client_handler(connection):
    client_cmd_handler = ClientCommandHandler()
    connection.send(str.encode(f'You are now connected to the server...\nType {EXIT_MESSAGE} to exit.\nType help or ? for command list.'))
    while True:
        data = connection.recv(2048)
        message = data.decode('utf-8')
        print("message:", message)
        if message == EXIT_MESSAGE:
            connection.sendall(str.encode(EXIT_MESSAGE))
            break
        reply = client_cmd_handler.onecmd(message) or "invalid command"
        connection.sendall(str.encode(reply))
    connection.close()

def proxy_handler(connection):
    proxy_cmd_handler = ProxyCommandHandler()
    connection.send(str.encode(f'You are now connected to the server...\nType {EXIT_MESSAGE} to exit.\nType help or ? for command list.'))
    while True:
        data = connection.recv(2048)
        message = data.decode('utf-8')
        if message == EXIT_MESSAGE:
            connection.sendall(str.encode(EXIT_MESSAGE))
            break
        reply = proxy_cmd_handler.onecmd(message) or "invalid command"
        connection.sendall(str.encode(reply))
    connection.close()

def accept_connections(ssocket, handler=client_handler):
    Client, address = ssocket.accept()
    print(f'Connected to: {address[0]}:{str(address[1])}')
    start_new_thread(handler, (Client, ))

server_socket_c = socket.socket()  # client
server_socket_p = socket.socket()  # proxy
try:
    server_socket_c.bind((HOST, PORT))
    server_socket_p.bind((HOST, PORT_P_MAIN_SERVER))
except socket.error as e:
    print(f"An error occured {str(e)}")

print(f'Server is listing for the proxy on the port {PORT_P_MAIN_SERVER}...')
server_socket_p.listen()
accept_connections(server_socket_p, proxy_handler)

print(f'Server is listing for clients on the port {PORT}...')
server_socket_c.listen()

while True:
    accept_connections(server_socket_c)
