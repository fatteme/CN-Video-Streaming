import socket

from constraints import HOST, PORT, EXIT_MESSAGE, PORT_P_PROXY_SEREVR

client_socket = socket.socket()
proxy_socket = socket.socket()

print('Waiting for connection...')
try:
    client_socket.connect((HOST, PORT))
    proxy_socket.connect((HOST, PORT_P_PROXY_SEREVR))
except socket.error as e:
    print(f"An error occurred {str(e)}")
    exit()

response = client_socket.recv(1024)
decoded_res = response.decode('utf-8')
print(f"{decoded_res}")

response = proxy_socket.recv(1024)
decoded_res = response.decode('utf-8')
print(f"{decoded_res}")

mode = input("Please input the executing mode (user/admin)")
if mode == 'user':
    while True:
        Input = input('Your command: ')
        if not Input:
            continue
        client_socket.send(str.encode(Input))
        response = client_socket.recv(1024)
        decoded_res = response.decode('utf-8')
        if(decoded_res == EXIT_MESSAGE):
            break
        print(f"{decoded_res}")
elif mode == 'admin':
    while True:
        Input = input('Your command: ')
        if not Input:
            continue
        proxy_socket.send(str.encode(Input))
        response = proxy_socket.recv(1024)
        decoded_res = response.decode('utf-8')
        if(decoded_res == EXIT_MESSAGE):
            break
        print(f"{decoded_res}")

client_socket.close()
proxy_socket.close()
