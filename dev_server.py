import tornado.ioloop
import tornado.web
import argparse
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
        self.write("This is the welcome screen")

class PostHandler(tornado.web.RequestHandler):
    def get(self):
    	"""
		Should provide a default message, (please POST to this service)
    	"""
        self.write("This is how you submit jsons")

    def post(self):
    	"""
		make sure to get the data from the post
    	"""
    	data = self.request.body
        self.write("you've written a json")	
	

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/submit", PostHandler),
    ])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'webserver framework')
    parser.add_argument('-p', help = 'port we will run server as', default=7777)
    args = parser.parse_args()

    app = make_app()
    app.listen(args.p)
    tornado.ioloop.IOLoop.current().start()