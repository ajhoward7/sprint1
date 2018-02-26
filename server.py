from flask import Flask, request
import subprocess

import logging
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)

# Setting up the logger:
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler("test.log",
                                   when="m",
                                   interval=2,
                                   backupCount=5)
logger.addHandler(handler)


@app.route('/', methods=['GET', 'POST'])
def parse_request():
    data = request.json  # Take JSON data from HTTP

    logger.info(data)  # log

    return "Here, have some HTML in return\n"

@app.route('/test')
def test_connection():
    return "Server running!\n"

@app.route('/shutdown')
def shutdown():
    subprocess.call("pkill gunicorn", shell = True)
    return "Process shutting down..."
