#!/usr/local/bin/python
# script to remove all MACs older than 12 hours
# add this to
import db as database
from iptables import IPTables

ipt = IPTables()
db = database.DB()
maxtime = 60 *720
# remove all MACs older than 12 hours from db and iptables
for mac in db.getMACs():
    d = db.getTimeDeltaForMAC(mac)
    if d > maxtime:
        print("removed: " + mac)
        db.rmMAC(mac)
        ipt.lockMAC(mac)
