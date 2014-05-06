#!/usr/local/bin/python
# script to remove all MACs older than 12 hours
# add this to
import time
import db as database
from iptables import IPTables
import tables

ipt = IPTables()
db = database.DB()
# remove all MACs older than 12 hours from db and iptables
for row in db.getExpiredMACs():
    mac = row.mac
    print("removed: " + mac)
    db.rmMAC(mac)
    ipt.lockMAC(mac)
