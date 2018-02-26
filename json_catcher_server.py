from flask import Flask, request
import subprocess
from json_processing import extract_fields
import logging
import os
from logging.handlers import TimedRotatingFileHandler

#################################################################
#
#         APP
#
#################################################################


"""
Purpose: this is a JSON Catcher app
1. will receive POST requests with JSON strings as the payload
2. will log all requests
3. and if valid json strings, will extract name and age information
to be stored.

MAIN paths:

POST http://json_server/ 
GET http://json_server/test  - will return a note if its running
GET http://json_server/shutdown - will shut down server remotely, even if running
    on either Flask or Gunicorn
"""

app = Flask(__name__)

#################################################################
#
#         LOGGERS
#
#################################################################

def create_logger(logger_name, log_file_path):
    """
    Used to create a logging object
    since the objectives of this project are fixed
    will hard code the interval
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(log_file_path,
                                       when="m",
                                       interval=2,
                                       backupCount=5)
    logger.addHandler(handler)
    return logger

# create the raw logger for ALL requests
raw_logger = create_logger('raw logger', './raw.txt')

# create the proc logger for all processed requests
proc_logger = create_logger('proc logger', './proc.txt')



#################################################################
#
#         WEB HANDLERS
#
#################################################################


@app.route('/', methods=['GET', 'POST'])
def parse_request():
    """
    Take JSON data from HTTP
    
    using request.data, because request.json will crash the server
    if the POST request is not formatted correctly
    to be more robust, will take in data as a string and verify the
    content type
    
    Note that the json_processing.EXTRACT_FIELDS function will do None and '' handling in strings
    """

    # catch any post request and log, regardless of validity
    data = request.data  
    raw_logger.info(data)  # log

    # Check content type before parsing
    content_type = request.headers['Content-Type']
    if content_type != 'application/json':
        return "Incorrect payload type, please submit 'application/json'"
    
    # using json_processing library
    name_and_age = extract_fields(data)

    # construct output message
    response_msg = "Successfully submitted:\n %s" % (data)

    # if valid data
    if name_and_age is not None:
        proc_logger.info(name_and_age)
        response_msg += "\n Found Name and Age: %s" % name_and_age

    return response_msg


@app.route('/test')
def test_connection():
    """
    Used for testing if the server is up, returns simple message
    """
    return "Server running!\n"


@app.route('/shutdown')
def shutdown():
    """
    Used for shutting down the server remotely. This calls the underlying
    platform and forces a shutdown. 
    
    # subprocess.call("pkill gunicorn", shell = True)
    """
    
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        # if running on gunicorn
        os._exit(4)
    else:
        # if running python server.py (using werkzeug)
        func()
    return "Process shutting down..."



"""
Uncomment this line to run for local testing instead of gunicorn
python server.py
"""
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)