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

    def addMAC(self, mac, longterm=False):
        try:
            expire = time.time() + 3600 * (24 * 90 if longterm else 12)
            self.session.add(tables.Clients(mac=mac, time=time.time(), expire=expire))
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

    def removeExpired(self):
        now = time.time()
        res = self.session.query(tables.Clients).filter(tables.Clients.expire < now)
        for row in res:
            self.session.delete(row)
        self.session.commit()

    def getExpiredMACs(self):
        now = time.time()
        res = self.session.query(tables.Clients).filter(tables.Clients.expire < now)
        return res

    def getMACs(self):
        res = self.session.query(tables.Clients.mac).all()
        list = [e[0] for e in res]
        return list

if __name__ == '__main__':
        pass
