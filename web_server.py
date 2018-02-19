import tornado.ioloop
import tornado.web
from json_processing import *

"""
JSON Nibbler Webservice

Starts a json ingestion API service, other services can
connect and submit jsons that will be checked for formatting
then logged. 
"""

class MainHandler(tornado.web.RequestHandler):
    def get(self):
    	"""
		Should provide a default welcome service (README)
		will provide the proper way to submit data
    	"""
        self.write("Hello, world")

class PostHandler(tornado.web.RequestHandler):
    def get(self):
    	"""
		Should provide a default message, (please POST to this service)
    	"""
        self.write("Hello, world")

    def post(self):
    	"""
		make sure to get the data from the post
    	"""
    	data = self.request.body
        self.write("Hello, world")	
	

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/submit", PostHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()