import tornado.ioloop
import tornado.web
import json
import logging
import time
from logging.handlers import RotatingFileHandler
from catcher_handlers import JSONHandler, StopHandler

"""
WEB APP

Creates an web app that accepts JSON post requests, hosted by
Tornado App. 
"""


# reads open the stop key password
with open('./stop_key.txt', 'r') as f:
	STOP_KEY = f.read().strip()


def create_logger(path, name='my logger'):
	"""
	Initializes the logger, and returns logging object to be used
	in web page. the PATH is the name of the logging file that will
	be made.

	Will use twice to:
	1. make the RAW LOGGER
	2. make the PROC LOGGER
	"""
	handler = logging.handlers.TimedRotatingFileHandler(path, when="S", 
		interval=10, 
		backupCount=10)
	
	logger = logging.getLogger(name) # or pass string to give it a name
	logger.setLevel(logging.INFO)
	logger.addHandler(handler)

	return logger
		

def make_app(raw_logger, proc_logger):
    """ 
    Assigns the different python methods to each path
    Additional paths can be handled if added

    server/ 		<- handles json
    server/stop 	<- requires a password, but can stop server
    """
    return tornado.web.Application([
        (r"/", JSONHandler, {'proc_logger': proc_logger, 'raw_logger': raw_logger}),
        (r"/stop", StopHandler),
    ])


if __name__ == "__main__":
	""" 
	main method, starts the webserver from the commandline 
	"""
	raw_logger = create_logger('./Raw.txt', 'raw_logger')
	proc_logger = create_logger('./proc.txt', 'proc_logger')

	print('Starting the JSON Catching server....')
	app = make_app(raw_logger, proc_logger)

	print('Server started....')
	app.listen(9000)

	tornado.ioloop.IOLoop.current().start()