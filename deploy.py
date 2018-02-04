import paramiko
import sys
from os.path import expanduser
import time
import json
import argparse

def connect(key_url, server_url, username='ec2-user'):
    """
    used for connecting to a server, takes in a server
    and a password and returns a logged in client
    """
    server = server_url
    k = paramiko.RSAKey.from_private_key_file(key_url)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print "connected to %s " % server_url
    c.connect(hostname = server, username = username)
    return c


def get_timestamp():
    """
    Simply returns a timestamp, used for logging
    """
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())


def check_log(client):
    msg = 'opened connection at %s' % get_timestamp()    
    while True:
        _, stdout, _ = client.exec_command('cat flock_log.log | wc -l')
        line_count = int(stdout.read().split('\n')[0])
        if line_count % 2 == 0:
            print "%d Logs found" % line_count
            client.exec_command("echo %s > flock_log.log" % msg )
            break
        print "..."
        time.sleep(10)
    print "no other connections"


def git_pull(client):
    """
    git clones a directory
    """
    try:
        client.exec_command("cd ~/; git clone https://github.com/ajhoward7/sprint1.git")
        print 'repository created'
    except Exception as e:
        print e

        
def update_crontab(client, prefix):
    print "initializing crontab script for '%s'" % prefix
    msg = '* * * * * python /home/ec2-user/sprint1/json_digest.py'
    try:
        client.exec_command('crontab -r')
        #client.exec_command('crontab -l | {cat; echo "%s"; } | crontab -' % msg)
        client.exec_command('(crontab -l 2>/dev/null; echo "*/5 * * * * python /home/ec2-user/sprint1/json_digest.py --prefix %s") | crontab -' % prefix)
        print 'cron tab updated'
    except Exception as e:
        print(e)
        

def clean_up(client):
	client.exec_command('rm -r ~/sprint1')


def deploy(key_url, server_url, prefix):
	c = connect(key_url, server_url)
	git_pull(c)
	update_crontab(c, prefix)


parser = argparse.ArgumentParser(description = 'json ingestion library')
parser.add_argument('-k', help = 'location of the server pem key')
parser.add_argument('-s', help = 'server we are connecting to')
parser.add_argument('-p', help = 'file prefix that we will be searching for ')
args = parser.parse_args()


if __name__ == '__main__':

	with open('/Users/timlee/Dropbox/keys/sprint_key.txt','rb') as f:
		server_url, key_url = f.read().split(',') 

	if args.k is not None:
		key_url = args.k

	if args.s is not None:
		server_url = args.s

	if args.p is not None:
		prefix = args.p
	else:
		prefix = 'ppp'

		
	deploy(key_url, server_url, prefix)