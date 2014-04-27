import re

class Helper(object):
    def getMAC(self, ip):
        with open('/proc/net/arp') as arp:
            for line in arp:
                if re.search(ip, line):
                    return line.split()[3]

if __name__ == '__main__':
        pass
