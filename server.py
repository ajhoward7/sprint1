from flask import Flask, request

import logging
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def parse_request():
    data = request.json
    data = " ".join(data.split("\n"))  # remove hard returns

    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler("test.log",
                                       when="m",
                                       interval=2,
                                       backupCount=5)
    logger.addHandler(handler)

    logger.info(data)

    return "Here, have some HTML in return\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)