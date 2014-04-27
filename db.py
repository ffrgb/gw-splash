from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, mapper
import sqlalchemy.exc
import tables
import time

class DB(object):
    def __init__(self):
        Session = sessionmaker(bind=tables.engine)
        self.session = Session()

    def checkRecordExists(self, mac):
        if not (self.session.query(tables.Clients).filter(tables.Clients.mac == mac).first() == None):
            return True
        else:
            return False

    def addMAC(self, mac):
        try:
            self.session.add(tables.Clients(mac = mac, time = time.time()))
            self.session.commit()
        except:
            raise

    def rmMAC(self, mac):
        try:
            res = self.session.query(tables.Clients).filter(tables.Clients.mac == mac).one()
            self.session.delete(res)
            self.session.commit()
        except:
            raise

    def getTimeDeltaForMAC(self, mac):
        res = self.session.query(tables.Clients.time).filter(tables.Clients.mac == mac).scalar()
        now = time.time()
        return now - res

    def removeOlderThan(self, minutes):
        now = time.time()
        sec = minutes*60
        tdelta = now - sec
        res = self.session.query(tables.Clients).filter(tables.Clients.time < tdelta)
        for row in res:
            self.session.delete(row)
        self.session.commit()

if __name__ == '__main__':
        pass
