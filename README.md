# Sprint2 Library: 

*Team SELECT STARS: Alex Howard, Patrick Yang, Jade Yun, Tim Lee*

## Architecture
```
"""
# -------------#
# -------------#
# ----LAPTOP---#
# -------------#   ----> deploy.py -->  # -------------#
# -------------#                        # -------------#
        |                               # -----AWS-----#
       deploy.py                        # --WEBSERVER--#
        |                               # -------------#
# -------------#  ---> JSON POSTS ->    # -------------#
# -------------#                        # -------------#
# -TEST SERVER-#                            - processes valid json
# -------------#                            - logs all requests RAW
# -------------#                            - records locally in PROC
"""
```

#### How to run:
```python
deploy('path_to_ssh_private_key.pem', 'server-address','prefix')
```
#### Files
```
|- archive_old_versions/			# our earlier prototypes/ different platforms
|- phase1/ 							# our simple json processing program
|- sample_json_generator/ 			# scripts to simulate input data coming in
|--- deploy_server.py				# main deployment python script
|--- json_catcher_server.py		# does what it says, catches jsons
|--- json_processing.py				# lib to validate and extract data from json
|--- stop_remote_aws_server.py	# stops the server on AWS
```

#### Deployment Specifications:
- Remotely deploys this repo to a AWS instance
- Ensure that the ports are configured correctly with security
- Python: starts a Flask application that accepts HTTP post requests


#### API Webservice Specifications:
- Accepts raw data within the body (POST), expect formatted jsons
- Request Log (successful or not) `/srv/runme/prefix/Raw.txt`
- Use a logrotate or `TimedRotatingFileHandler` to rotate the file every 2 minutes into another file within the same directory
- If request is valid, then process into `/srv/runme/prefix/proc.txt`
- `prefix` will be passed to deploy function which will define the name of your output file


#### Testing service:
- Server #2 will test server #1 by sending repeated JSON posts
- Test Send Server: generate and send good and bad jsons 

#### [Reference PDF](Sprint2.pdf)

#### Library Options:
- Flask
- Tornado (also python)

### Project Planning, key tasks:

|Task | Assignment|
|-----------| ----|
|retrofit deploy| Tim|
|write the webpaths for requests| Alex|
|logging of web requestes| Patrick|
|create test server (to send)| Jade|


#### Notes:

- Helpful to check web API and apps: [https://www.getpostman.com/](https://www.getpostman.com/)