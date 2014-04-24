from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///clients.db')
Base = declarative_base()

class Clients(Base):
    __tablename__ = 'clients'

    clientID = Column(Integer, primary_key=True)
    mac = Column(String, unique=True)
    time = Column(String)

# create tables
Base.metadata.create_all(engine)

