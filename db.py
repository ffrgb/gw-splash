from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///nodes.db')
Base = declarative_base()

class Nodes(Base):
    __tablename__ = 'nodes'

    clientID = Column(Integer, primary_key=True)
    mac = Column(String, unique=True)
    time = Column(String)

# create tables
Base.metadata.create_all(engine)

