# ===============================================================
# Team select stars
# 
# Tim Lee
# Jade Yun
# Patrick Yang
# Alex Howard
# ===============================================================

import paramiko
import requests
import sys
import subprocess

"""
These are all the connection libraries related to deploying code
on a AWS instance. It is assumed that the AWS instance should 
already be setup, running, and all accounts have the correct 
permissions for writing files. 

The working directory that will be used is :
/srv/runme/ 

Please ensure that the correct permissions are set
for this directory as it is not at the user level

GOAL :  Simple remote deployment of a webserver on AWS
1. connect to aws instance
2. install/update necessary python software for API service
3. start the webservice
4. test that the webservice is receiving input
5. disconnect
"""

def connect(key_url, server_url, username='testtest'):
    """
    Input:
    - key_url: STRING the local system path location of the private key
    - server_url: STRING  the URL of the server that the repo will be deployed to
    - username: (OPTIONAL) STRING will be the user that connects, 
    such as ubuntu@server.ip, ec2-user@server.ip

    Returns:
    - Web connection client
    """

    # create key and client
    k = paramiko.RSAKey.from_private_key_file(key_url)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
    print "connected to %s " % server_url
    c.connect(hostname = server_url, username = username, pkey = k)

    # return an abstracted client
    return c


def client_bash(client, command, verbose=True):
    """
    small wrapper for ssh client calls, always want to print
    console in and console errors, will save from printing 
    every single time
    """
    stdin,stdout,stderr = client.exec_command(command)        
    
    if verbose:
        print '\n'.join(stdout.readlines()), '\n'.join(stderr.readlines())
    return client


def install_code_repo(client, deploy_repo='https://github.com/ajhoward7/sprint1.git'):
    """
    Input: a ssh connection, designed around a paramiko object

    Function will do the following:
    1. check to see if the repo exists
    2. if not, pulls for first time with 'git clone'
    3. if already pulled, will re-pull with 'git pull' for latest version

    Defaults to the main repo, but can be reset for a different folder, or different repo
    """
    install_folder = deploy_repo.split('/')[-1].split('.git')[0]

    _, stdout, _ = client.exec_command("ls ~/")
    files = stdout.read()
    
    try:
        if 'sprint1' in files:
            client_bash(client, "cd ~/%s; git pull" % install_folder)       
            #client_bash(client, "cd ~/%s; git checkout master" % install_folder)  # DELETE LATER - for testing 
            print 'repository repulled'
        else:
            client_bash(client,"cd ~/; git clone %s" % deploy_repo )
            print 'repository created'
        
    except Exception as e:
        print e



        
def start_webserver(client, prefix):
    """
    Assuming the appropriate repo has been installed
    run the web_server.py to star the service
    """
    bash_cmd = 'cd ~/sprint1;gunicorn -D --threads 4 -b 0.0.0.0:8080 server:app %s' % prefix
    client_bash(client, bash_cmd, verbose=True)
    print "web server started"



def test_webserver_connection(web_url):
    """
    input : web_url : STRING - the url of where the webserver is running
    performs simple web test to ensure that web service is running
    """
    try:
        resp = requests.get(web_url)
        if resp.status_code == 200:
            print "Webservice is running"
        else:
            print "Webservice status: %s" %resp.status_code
    except Exception as e:
        print(e)


def check_url_exists(url):
    try:
        resp = requests.get(url)
        return resp.status_code == 200
    except:
        return False


def deploy(key_url, server_url, prefix):
    """
    This is the main deploy script that does the following:
    1. connects to the server
    2. < installs some code >
    3. < 
    """
    status_url = 'http://%s:8080/test' % server_url
    
    if check_url_exists(status_url):
        print "server already running, stopping then reinstalling"
        try:
            resp = requests.get('http://%s:8080/shutdown' % server_url)
        except:
            # request will error out since server shuts down
            pass

    try:
        c = connect(key_url, server_url)
        install_code_repo(c)
        start_webserver(c, prefix)
        c.close()

    except KeyboardInterrupt:
        requests.get(server_url+':8080/shutdown')

