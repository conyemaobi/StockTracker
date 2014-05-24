#!python
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Timestamp
engine = create_engine('mysql://root:password@localhost/somedb', echo=False)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Stocks(Base):
	__tablename__ = 'stocks'
	id = Column(Integer, primary_key=True)
	stock = Column(String(30), nullable=False)
	count = Column(Integer, nullable=False)
	last_modified = Column(Timestamp, nullable=False)

def __repr__(self):
    return "<Stocks('%s')>" % (self.stock)

users_table = Stocks.__table__
metadata = Base.metadata

def create_all():
    metadata.create_all(engine)
