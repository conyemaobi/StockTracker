from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
import tornado.escape
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import func
from models import * 
import psycopg2
import json
import passwords

class MainHandler(RequestHandler):
  def get(self):
	#conn = psycopg2.connect(database=passwords.Live.database, user=passwords.Live.user, password=passwords.Live.password, host=passwords.Live.host, port=passwords.Live.port)
	#cur = conn.cursor()
        #cur.execute("SELECT stock,count from STOCKS where count > 3 order by stock asc limit 40")
        #rows = cur.fetchall()
	db = scoped_session(sessionmaker(bind=engine))
	rows = db.query(Mention).with_entities(Mention.stock, func.count(Mentions).label('total')).group_by(Mention.stock).order_by('total ASC').limit(40)
	#.filter_by(first_name="mark").all()
	self.write('callback(' + json.dumps(rows) + ')')
        self.set_header('Content-Type', 'application/javascript')
	conn.close()

application = Application([
(r"/", MainHandler)
])

if __name__ == "__main__":
  application.listen(5000)
  IOLoop.instance().start()
