from subprocess import call

class IPTables(object):
    def __init__(self):
        self.destination = '10.142.0.1'
        self.port = '5000'
        self.mark = '99'
        self.chain = 'portal'
        self.iface = 'bat0'

    def start(self):
        call(['iptables', '-N', self.chain, '-t', 'mangle'])
        call(['iptables', '-t', 'mangle', '-A', 'PREROUTING', '-i', self.iface, '-j', self.chain])
        call(['iptables', '-t', 'mangle', '-A', self.chain, '-j', 'MARK', '--set-mark', self.mark])
        call(['iptables', '-t', 'nat', '-A', 'PREROUTING', '-i', self.iface , '-m', 'mark', '--mark', self.mark, '-p', 'tcp', '--dport', '80', '-j', 'DNAT', '--to-destination', self.destination+':'+self.port])
        call(['iptables', '-t', 'filter', '-A', 'FORWARD', '-m', 'mark', '--mark', self.mark, '-j', 'DROP'])

    def shutdown(self):
        call(['iptables', '-t', 'mangle', '-D', 'PREROUTING', '-i', self.iface, '-j', self.chain])
        call(['iptables', '-t', 'mangle', '-F', self.chain])
        call(['iptables', '-t', 'mangle', '-X', self.chain])
        call(['iptables', '-t', 'filter', '-D', 'FORWARD', '-m', 'mark', '--mark', self.mark, '-j', 'DROP'])
        call(['iptables', '-t', 'nat', '-D', 'PREROUTING', '-i', self.iface , '-m', 'mark', '--mark', self.mark, '-p', 'tcp', '--dport', '80', '-j', 'DNAT', '--to-destination', self.destination+':'+self.port])

    def unlockMAC(self, mac):
        if not call(['iptables', '-t', 'mangle', '-I', self.chain, '-m', 'mac', '--mac-source', mac, '-j', 'RETURN']):
            return True
        else:
            return False

    def lockMAC(self, mac):
        res = call(['iptables', '-t', 'mangle', '-D', self.chain, '-m', 'mac', '--mac-source', mac, '-j', 'RETURN'])
        if res:
            return True
        else:
            return False
    def unlockDNS(self, ip):
        if not call(['iptables', '-t', 'mangle', '-I', self.chain, '-d', ip, '-j', 'RETURN']):
            return False

    def unlockDHCP(self, ip):
        if not call(['iptables', '-t', 'mangle', '-I', self.chain, '-d', ip, '-p udp', '--dport', '67:68', '--sport', '67:68', '-j', 'RETURN']):
            return False


if __name__ == '__main__':
    pass
