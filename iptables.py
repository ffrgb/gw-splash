from subprocess import call

class IPTables(object):
    def __init__(self):
        self.destination = '10.142.0.1'
        self.destinationv6 = '[2a01:4f8:100:57ff::1]'
        self.port = '5000'
        self.mark = '99'
        self.chain = 'portal'
        self.iface = 'bat0'

    def __start(self, iptables, destination):
        call([iptables, '-N', self.chain, '-t', 'mangle'])
        call([iptables, '-t', 'mangle', '-A', 'PREROUTING', '-i', self.iface, '-j', self.chain])
        call([iptables, '-t', 'mangle', '-A', self.chain, '-j', 'MARK', '--set-mark', self.mark])
        if iptables not 'ip6tables':
            call([iptables, '-t', 'nat', '-A', 'PREROUTING', '-i',self.iface , '-m', 'mark', '--mark', self.mark, '-p', 'tcp', '--dport', '80', '-j', 'DNAT', '--to-destination', destination+':'+self.port])
        call([iptables, '-t', 'filter', '-A', 'FORWARD', '-m', 'mark', '--mark', self.mark, '-j', 'DROP'])

    def __shutdown(self, iptables, destination):
        call([iptables, '-t', 'mangle', '-D', 'PREROUTING', '-i', self.iface, '-j', self.chain])
        call([iptables, '-t', 'mangle', '-F', self.chain])
        call([iptables, '-t', 'mangle', '-X', self.chain])
        call([iptables, '-t', 'filter', '-D', 'FORWARD', '-m', 'mark', '--mark', self.mark, '-j', 'DROP'])
        if iptables not 'ip6tables':
            call([iptables, '-t', 'nat', '-D', 'PREROUTING', '-i',self.iface , '-m', 'mark', '--mark', self.mark, '-p', 'tcp', '--dport', '80', '-j', 'DNAT', '--to-destination', destination+':'+self.port])

    def __unlockMAC(self, iptables, mac):
        if not call([iptables, '-t', 'mangle', '-I', self.chain, '-m', 'mac', '--mac-source', mac, '-j', 'RETURN']):
            return True
        else:
            return False

    def __lockMAC(self, iptables, mac):
        res = call([iptables, '-t', 'mangle', '-D', self.chain, '-m', 'mac', '--mac-source', mac, '-j', 'RETURN'])
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

    def start(self):
        self.__start('iptables', self.destination)
        self.__start('ip6tables', self.destinationv6)

    def shutdown(self):
        self.__shutdown('iptables', self.destination)
        self.__shutdown('ip6tables', self.destinationv6)

    def unlockMAC(self, mac):
        if self.__unlockMAC('iptables', mac) and self.__unlockMAC('ip6tables', mac):
            return True
        else:
            return False

    def lockMAC(self, mac):
        self.__lockMAC('iptables', mac)
        self.__lockMAC('ip6tables', mac)

if __name__ == '__main__':
    pass
