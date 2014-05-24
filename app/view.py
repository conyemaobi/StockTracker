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
        id = db.Column(db.Integer, db.Sequence('mention_id', start=1, increment=1), primary_key=True)
        stock = db.Column(db.String(30), nullable=False)
        mention_time = db.Column(TIMESTAMP, nullable=False)

        def __init__(self, stock, mention_time):
                self.stock = stock
                self.mention_time = mention_time

        def __repr__(self):
                return "<Mention('%s')>" % (self.stock, self.mention_time)

##### SERIALIZERS #####

class MentionSerializer(Serializer):

    class Meta:
        fields = ("id", "stock", "mention_time")

##### API #####

@app.route('/api/v1/mentions', methods=["GET"])
def data():
        #rows = db.query(Mention).with_entities(Mention.stock, func.count(Mention).label('total')).group_by(Mention.stock).order_by('total ASC').limit(40)
	mentions = Mention.query.all()
	return jsonify({"mentions": MentionSerializer(mentions, many=True).data})
