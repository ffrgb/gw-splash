#sorry but for now we need this starter script
from iptables import IPTables
import db as database

db = database.DB()
ipt = IPTables()

ipt.start()
ipt.unlockDNS('188.40.255.242')
ipt.unlockDNS('213.73.91.35')

db.removeOlderThan(720)
for mac in db.getMACs():
    ipt.unlockMAC(mac)
