import socket

from Constants import HOST, PORT, EXIT_MESSAGE

ClientSocket = socket.socket()

print('Waiting for connection...')
try:
    ClientSocket.connect((HOST, PORT))
except socket.error as e:
    print(f"An error occurred {str(e)}")
    exit()

Response = ClientSocket.recv(1024)
decodedRes = Response.decode('utf-8')
print(f"{decodedRes}")
while True:
    Input = input('Your command: ')
    if not Input:
        continue
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    decodedRes = Response.decode('utf-8')
    if(decodedRes == EXIT_MESSAGE):
        break
    print(f"{decodedRes}")

ClientSocket.close()
