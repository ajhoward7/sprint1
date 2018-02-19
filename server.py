from flask import Flask, request

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
    print data
    #data = " ".join(data.split("\n"))  # remove hard returns

    logger.info(data)  # log

    return "Here, have some HTML in return\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)