from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
import os

pack_dir = os.path.dirname(os.path.abspath(__file__))
engine = create_engine('sqlite:////' + os.path.join(pack_dir, 'clients.db'))
Base = declarative_base()

class Clients(Base):
    __tablename__ = 'clients'

    clientID = Column(Integer, primary_key=True)
    mac = Column(String, unique=True)
    time = Column(Float)
    expire = Column(Float)

# create tables
Base.metadata.create_all(engine)

