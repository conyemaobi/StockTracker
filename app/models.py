#!python
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.types import TIMESTAMP, FLOAT
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
import passwords

Base = declarative_base()
engine = create_engine('postgresql+psycopg2://'+passwords.Live.username+':'+passwords.Live.password+'@'+passwords.Live.hostname+':5432/'+passwords.Live.db, echo=False)

class Mention(Base):
	__tablename__ = 'mention'
	id = Column(Integer, primary_key=True)
	stock = Column(String(30), nullable=False)
	#count = Column(Integer, nullable=False)
	current_timestamp = Column(TIMESTAMP, nullable=False)
	
	def __init__(self, stock, current_timestamp):
        	self.stock = stock
        	self.current_timestamp = current_timestamp

	def __repr__(self):
		return "<Mention('%s')>" % (self.stock, self.current_timestamp)

mention_table = Mention.__table__
metadata = Base.metadata

def create_all():
    metadata.create_all(engine)
