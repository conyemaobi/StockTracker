from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.types import TIMESTAMP, FLOAT
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import func
from marshmallow import Serializer, fields
import psycopg2
import json
import passwords
from collections import OrderedDict

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

class MentionCountSerializer(Serializer):

    class Meta:
        fields = ('stock', 'total')

##### API #####

@app.route('/api/v1/mentions', methods=["GET"])
def data():
	serializer = None
	if request.args.get('function') == "count":
		mentions = db.engine.execute("select stock, count(*) as mention_total from mention group by stock order by mention_total asc limit 40").fetchall()
		serializer = [{"stock" : i[0], "mention_count" : i[1]} for i in mentions]
	else:
		mentions = Mention.query.all()
		serializer = MentionSerializer(mentions, many=True).data

	if request.args.get('output') == "jsonp":
		return Response('callback('+json.dumps({"mentions": serializer})+')', content_type='application/javascript')
	else:
		return jsonify({"mentions": serializer})
