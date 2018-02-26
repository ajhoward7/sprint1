import tornado.web
from json_processing import extract_fields

"""
WEB HANDLERS

These are the two web handlers used in the web app. 

JSONHandler - absorbs POST requests json
StopHandler - takes requests to stop the server

"""


class JSONHandler(tornado.web.RequestHandler):
	"""
	Main JSON handler, receives 
	HEAD - gives status
	GET - gives information
	POST - accepts JSON and records on ther current server

	"""
	def initialize(self, raw_logger, proc_logger):
		"""
		When the JSON Handler is created, assign the handler
		both logger objects.
		"""
		self._raw_logger = raw_logger
		self._proc_logger = proc_logger


	def head(self):
		"""
		Implements a status check. Only returns status code
		Used on the bash script to check if the server is running
		"""
		self.set_status(200)


	def get(self):
		"""
		Prints the default welcome message if browsed, (supposed to use POST)
		"""
		self.set_status(200)
		self.write("Welcome to the JSON catcher. Please POST a valid json to this server url")

	
	def post(self):
		"""
		Handles the json request. Should have Content-Type of application/json
		Then uses json_processing.py to handle the format checking
		"""

		# checks the type of submission
		content_type = self.request.headers['Content-Type']
		if content_type != 'application/json':
			self.set_status(400)
			self.write('please submit json formatted payloads, with "application/json" type ')

		else:
			try:
				payload = self.request.body

				# process the json
				json_str = payload.decode('utf-8','ignore')
				json_data_str = extract_fields(json_str)


				# save to both files, raw and proc
				self.write('Submitted data: ' + str(json_data_str))
				self._raw_logger.info(json_str)

				if json_data_str is not None:					
					self._proc_logger.info(json_data_str)
				self.set_status(200)

			except Exception as e:
				self.set_status(400)
				self.write('please submit json formatted payloads: %s' % str(e))			



class StopHandler(tornado.web.RequestHandler):
	"""
	Handles remote termination of the json catcher server

	GET - provides information
	POST - accepts a json or text key to stop the server
	"""

	def get(self):
		"""
		returns general information about webpath
		"""
		self.write('please submit the correct stop key with POST request')
		self.set_status(400)


	def post(self):
		"""
		Accepts JSON posts, any post can either be plain text
		or it can be application/json. Either way the key is 
		extracted and check to shutdown 
		"""

		# Get the key from the post
		content_type = self.request.headers.get('Content-Type')
		print(content_type)

		if content_type =='text/plain':

			# if its a plan text submission
			stop_key = self.request.body
			stop_key = stop_key.decode('latin1','ignore').strip()

		elif content_type == 'application/json':
			
			# if its a json payload
			try:
				json_payload = json.loads(self.request.body)
				stop_key = json_payload.get('stop_key')
			except Exception as e:
				self.write('json formatting error: %s' % str(e))
				self.set_status(400)
				return
		else:
			stop_key = None
			
		# if no stop key is found
		if stop_key is None:
			self.write('Stop Key not submitted stop_key, please try again')
			self.set_status(400)
			return
			
		# check if stopkey is correct
		if stop_key == STOP_KEY:

			# proper the stop the json server
			self.set_status(200)
			self.write("stopping server")
			tornado.ioloop.IOLoop.instance().stop()
		else: 

			# keep server running
			self.write('Stop Key incorrect, please try again')
			self.set_status(400)