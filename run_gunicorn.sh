#!/bin/bash
gunicorn -D --threads 4 -b 0.0.0.0:8080 --access-logfile server.log --timeout 60 server:app