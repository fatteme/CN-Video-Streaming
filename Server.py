import socket
from _thread import *

from constants import EXIT_MESSAGE, HOST, PORT

ThreadCount = 0

def client_handler(connection):
    connection.send(str.encode(f'You are now connected to the replay server... Type {EXIT_MESSAGE} to exit.'))
    while True:
        data = connection.recv(2048)
        message = data.decode('utf-8')
        if message == EXIT_MESSAGE:
            connection.sendall(str.encode(EXIT_MESSAGE))
            break
        
        reply = f'{message}'
        connection.sendall(str.encode(reply))
    connection.close()

def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept()
    print(f'Connected to: {address[0]}:{str(address[1])}')
    start_new_thread(client_handler, (Client, ))

ServerSocket = socket.socket()
try:
    ServerSocket.bind((HOST, PORT))
except socket.error as e:
    print(f"An error occured {str(e)}")

print(f'Server is listing on the port {PORT}...')
ServerSocket.listen()
    
while True:
    accept_connections(ServerSocket)
