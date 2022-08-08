import socket
from consts import HOST, PORT, EXIT_MESSAGE, PORT_P_PROXY_SEREVR, PORT_P_MAIN_SERVER
from random import randint

from video_handler import ClientVideo

video_port = randint(1024, 65536)
audio_port = video_port + 1
while video_port in [PORT, PORT_P_PROXY_SEREVR, PORT_P_MAIN_SERVER] or audio_port in [PORT, PORT_P_PROXY_SEREVR, PORT_P_MAIN_SERVER]:
    video_port = randint(1024, 65536)
    audio_port = video_port + 1

mode = input("Please input the executing mode (user/admin)")

sckt = socket.socket()
if mode == 'user':
    video_client_service = ClientVideo()
    video_socket = socket.socket()
    audio_socket = socket.socket()

print('Waiting for connection...')
try:
    port = PORT_P_PROXY_SEREVR if mode == "admin" else PORT
    sckt.connect((HOST, port))
except socket.error as e:
    print(f"An error occurred {str(e)}")
    exit()

response = sckt.recv(1024)
decoded_res = response.decode('utf-8')
if(decoded_res == EXIT_MESSAGE):
    sckt.close()
    print("connection refused.")
    exit()
print(f"{decoded_res}")


def preprocess(command, sckt):
    keyword = command.split()[0]
    if keyword == "upload":
        video_socket.bind((HOST, video_port))
        audio_socket.bind((HOST, audio_port))
        video_socket.listen()
        audio_socket.listen()

        # 'upload [title] [ip] [video_port]
        command += f' {HOST} {video_port}'
        sckt.send(str.encode(command))

        video_client, _ = video_socket.accept()
        audio_client, _ = audio_socket.accept()

        name = command.split()[1]
        video_client_service.send(video_socket=video_client, audio_socket=audio_client, name=name)

        response = sckt.recv(1024)
        decoded_res = response.decode('utf-8')
        print(decoded_res)
        return True
    return False

while True:
    command = input('Your command: ')
    if not command:
        continue
    already_sent = preprocess(command, sckt)
    if not already_sent:
        sckt.send(str.encode(command))
        response = sckt.recv(1024)
        decoded_res = response.decode('utf-8')
        if(decoded_res == EXIT_MESSAGE):
            break
        print(f"{decoded_res}")

sckt.close()
if mode == 'user':
    video_socket.close()
    audio_socket.close()
