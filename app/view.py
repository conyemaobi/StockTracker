from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.types import TIMESTAMP, FLOAT
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import func
from marshmallow import Serializer, fields
import psycopg2
import json
import passwords

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://'+passwords.Live.username+':'+passwords.Live.password+'@'+passwords.Live.hostname+':5432/'+passwords.Live.db
db = SQLAlchemy(app)

##### MODELS #####

class Mention(db.Model):
        #__tablename__ = 'mention'
        id = db.Column(db.Integer, primary_key=True)
        stock = db.Column(db.String(30), nullable=False)
        #count = Column(Integer, nullable=False)
        current_timestamp = db.Column(TIMESTAMP, nullable=False)

        def __init__(self, stock, current_timestamp):
                self.stock = stock
                self.current_timestamp = current_timestamp

        def __repr__(self):
                return "<Mention('%s')>" % (self.stock, self.current_timestamp)

##### SERIALIZERS #####

class MentionSerializer(Serializer):

    class Meta:
        fields = ("id", "stock", "current_timestamp")

##### API #####

@app.route('/api')
def data():
        #rows = db.query(Mention).with_entities(Mention.stock, func.count(Mention).label('total')).group_by(Mention.stock).order_by('total ASC').limit(40)
	mentions = Mention.query.all()
	return jsonify({"mentions": MentionSerializer(mentions, many=True).data})
