#sorry but for now we need this starter script
from iptables import IPTables
import db as database

db = database.DB()
ipt = IPTables()

dns1 = '188.40.255.242'
dns2 = '213.73.91.35'

ipt.start()
ipt.unlockDNS(dns1)
ipt.unlockDNS(dns2)

db.removeExpired()
for mac in db.getMACs():
    ipt.unlockMAC(mac)
