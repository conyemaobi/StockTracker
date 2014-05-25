from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
from view import app
import json
import passwords

class MainHandler(RequestHandler):
  def get(self):
	self.write("working")

tr = WSGIContainer(app)

application = Application([
(r"/", MainHandler),
(r".*", FallbackHandler, dict(fallback=tr))
])

if __name__ == "__main__":
  application.listen(5000)
  IOLoop.instance().start()
