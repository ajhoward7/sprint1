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
# -TEST SERVER-#                            - Runs server.py
# -------------#                            - processes valid json
# -------------#                            - logs all requests RAW
												    - records locally in PROC
"""
```

#### How to run:

Here is an example of how to deploy the server

```python
deploy('path_to_ssh_private_key.pem', 'server-address','prefix')

connected to ec2-35-166-134-236.us-west-2.compute.amazonaws.com
Already up-to-date.
repository repulled
web server started
```

#### How to stop:

Since gunicorn is running in the background, here's an easy way to terminate the server remotely.

```python

python stop_aws_server.py server-address

	>checking for server ec2-35-166-134-236.us-west-2.compute.amazonaws.com
	>server already running, stopping

```


#### Files
|file/dir | desc|
|-----------| ----|
|`archive_old_versions/`| Previous prototype versions on different platforms|
|`phase1/`| All of sprint1's work, simple remote json processing |
|`sample_json_generator/`| scripts to generate synthetic json input data|
|`deploy.py`| deploy the `json_catcher` to aws|
|`json_processing.py`| utilities to validate incoming json and extract data|
|`server.py`| JSON ingestion web API built on flask|
|`stop_remote_aws_server.py`| stop the `json_catcher` remotely|

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