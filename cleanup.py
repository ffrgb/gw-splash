#!/usr/local/bin/python
# script to remove all MACs older than 12 hours
# add this to
import db as database
from iptables import IPTables

ipt = IPTables()
db = database.DB()
# remove all MACs older than 12 hours from db and iptables
for mac in db.getExpiredMACs():
    print("removed: " + mac)
    db.rmMAC(mac)
    ipt.lockMAC(mac)
