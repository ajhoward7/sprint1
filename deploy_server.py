# ===============================================================
# Team select stars
# 
# Tim Lee
# Jade Yun
# Patrick Yang
# Alex Howard
# ===============================================================

import paramiko
import sys

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


def install_code_repo(client, deploy_repo='https://github.com/ajhoward7/sprint1.git'):
    """
    Input: a ssh connection, designed around a paramiko object
    Function will do the following:
    1. check to see if the repo exists
    2. if not, pulls for first time with 'git clone'
    3. if already pulled, will re-pull with 'git pull' for latest version

    """
    install_folder = deploy_repo.split('/')[-1].split(.git)[0]

    _, stdout, _ = client.exec_command("ls ~/")
    files = stdout.read()
    
    try:
        if 'sprint1' in files:
            stdin,stdout,stderr = client.exec_command("cd ~/%s; git pull" % install_folder)        
            print 'repository repulled'
        else:
            stdin,stdout,stderr = client.exec_command("cd ~/; git clone %s" % deploy_repo )        
            print 'repository created'

        print '\n'.join(stdout.readlines()), '\n'.join(stderr.readlines())
    except Exception as e:
        print e


def install_crontab(client, crontab_str):
    """
    Input: 
    - client : a paramiko ssh client
    - crontab_str : a crontab string to be installed on the server

    # previous "*/5 * * * * python /home/testtest/sprint1/json_digest.py --prefix %s"

    Tries to install a crontab string on the server
    """
    print "initializing crontab script"
    
    try:
        stdin,stdout,stderr = client.exec_command('crontab -r')
        print '\n'.join(stdout.readlines()), '\n'.join(stderr.readlines())

        stdin,stdout,stderr = client.exec_command('(crontab -l 2>/dev/null; echo "%s") | crontab -' % crontab_str)
        print '\n'.join(stdout.readlines()), '\n'.join(stderr.readlines())
        print 'cron tab updated'
    except Exception as e:
        print(e)        




        
def start_webserver(client, prefix):
    """
    Assuming the appropriate repo has been installed
    run the web_server.py to star the service
    """
    print "webservice started"


def test_webserver_connection(web_url):
    """
    input : web_url : STRING - the url of where the webserver is running
    performs simple web test to ensure that web service is running
    """
    print "Webservice is running"


def deploy(key_url, server_url, prefix):
    """
    This is the main deploy script that does the following:
    1. connects to the server
    2. < installs some code >
    3. < 
    """
    c = connect(key_url, server_url)
    get_code_repo(c)
    print "script successfully deployed"
    c.close()

