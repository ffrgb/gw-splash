from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///clients.db')
Base = declarative_base()

class Clients(Base):
    __tablename__ = 'clients'

    clientID = Column(Integer, primary_key=True)
    mac = Column(String, unique=True)
    time = Column(Float)

# create tables
Base.metadata.create_all(engine)

