from datetime import datetime
class DDosHandler():
    # 10 requests per minute
    REQUEST_THRESHOLD = 10

    def __init__(self) -> None:
        self.ips = {}

    def checkDDos(self, ip):
        now = datetime.now()
        if (ip in self.ips) and  (now - self.ips[ip]['date']).total_seconds() < 60:
            print('chheckDDOS', (now - self.ips[ip]['date']).total_seconds() < 60)
            self.ips[ip]['number'] = self.ips[ip]['number'] + 1
            if(self.ips[ip]['number'] > DDosHandler.REQUEST_THRESHOLD) :
                print(f'DDOS attack is Detected, ip: {ip}')
                return True
        else:
            self.ips[ip]= {'number': 1, 'date':now}
        self.ips[ip]['date'] = now
        return False
