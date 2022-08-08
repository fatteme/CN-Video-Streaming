import socket
from consts import HOST, PORT, EXIT_MESSAGE, PORT_P_PROXY_SEREVR
from random import randint

from video_handler import ClientVideo

video_port = randint(1024, 65536)
audio_port = video_port + 1
while video_port in [PORT, PORT_P_PROXY_SEREVR, PORT_P_MAIN_SEREVR] or audio_port in [PORT, PORT_P_PROXY_SEREVR, PORT_P_MAIN_SEREVR]:
    video_port = randint(1024, 65536)
    audio_port = video_port + 1

client_socket = socket.socket()
proxy_socket = socket.socket()

video_socket = socket.socket()
audio_socket = socket.socket()

video_client = ClientVideo()

print('Waiting for connection...')
try:
    client_socket.connect((HOST, PORT))
    proxy_socket.connect((HOST, PORT_P_PROXY_SEREVR))
except socket.error as e:
    print(f"An error occurred {str(e)}")
    exit()

response = client_socket.recv(1024)
decoded_res = response.decode('utf-8')
if(decoded_res == EXIT_MESSAGE):
    client_socket.close()
    print("connection refused.")
    exit()
print(f"{decoded_res}")

response = proxy_socket.recv(1024)
decoded_res = response.decode('utf-8')
print(f"{decoded_res}")

mode = input("Please input the executing mode (user/admin)")
sckt = client_socket
if mode == 'admin':
    sckt = proxy_socket

def preprocess(command):
    keyword = command.split()[0]
    if keyword == "upload":
        video_socket.bind((HOST, video_port))
        audio_socket.bin((HOST, audio_port))
        name = command.split()[1]
        video_client.send(video_socket=video_socket, audio_socket=audio_socket, name=name)
        # 'upload [title] [ip] [video_port]
        command += f' {HOST} {video_port}'
    return command

while True:
    command = input('Your command: ')
    if not command:
        continue
    command = preprocess(command)
    sckt.send(str.encode(command))
    response = sckt.recv(1024)
    decoded_res = response.decode('utf-8')
    if(decoded_res == EXIT_MESSAGE):
        break
    print(f"{decoded_res}")

client_socket.close()
proxy_socket.close()
