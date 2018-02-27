import requests
import sys

"""
Simple python program used to stop remote JSON Catcher servers
"""

def check_url_exists(url):
    """
    Checks if server is up
    """
    try:
        resp = requests.get(url)
        return resp.status_code == 200
    except:
        return False


if __name__ == '__main__':

	# get the server from the command line input
	server_url = sys.argv[1]

	# check to see if server is running 
	print "checking for server %s " % server_url	
	status_url = 'http://%s:8080/test' % server_url

	# if it is STOP it 
	if check_url_exists(status_url):
		print "server already running, stopping"
		try:
			resp = requests.get('http://%s:8080/shutdown' % server_url)
		except:
			# request will error out since server shuts down
			sys.exit()