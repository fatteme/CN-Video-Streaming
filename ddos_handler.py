
class DDosHandler():
    REQUEST_THRESHOLD =  3

    def __init__(self) -> None:
        self.ips = {}

    def checkDDos(self, ip):
        print(self.ips)
        if ip in self.ips:
            self.ips[ip] = self.ips[ip] + 1
            if(self.ips[ip] > DDosHandler.REQUEST_THRESHOLD) :
                print(f'DDOS attack is Detected, ip: {ip}')
                return True
        else:
            self.ips[ip] = 1
        return False
