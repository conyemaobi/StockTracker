#!python
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.types import TIMESTAMP, FLOAT
from sqlalchemy.ext.declarative import declarative_base
import passwords

Base = declarative_base()
engine = create_engine('psycopg2://'+passwords.Live.username+':'+passwords.Live.password+'@'+passwords.Live.hostname+':5432/'+passwords.Live.db, echo=False)

class Stocks(Base):
	__tablename__ = 'stocks'
	#id = Column(Integer, primary_key=True)
	stock = Column(String(30), nullable=False)
	count = Column(Integer, nullable=False)
	last_modified = Column(Timestamp, nullable=False)

def __repr__(self):
    return "<Stocks('%s')>" % (self.stock)

stocks_table = Stocks.__table__
metadata = Base.metadata

def create_all():
    metadata.create_all(engine)
