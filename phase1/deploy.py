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

def connect(key_url, server_url, username='testtest'):
    """
    used for connecting to a server, takes in a server
    and a password and returns a logged in client
    """
    server = server_url
    k = paramiko.RSAKey.from_private_key_file(key_url)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print "connected to %s " % server_url
    c.connect(hostname = server, username = username, pkey = k)
    return c

def git_pull(client):
    """
    git clones a directory
    """
    _, stdout, _ = client.exec_command("ls ~/")
    files = stdout.read()
    
    try:
        if 'sprint1' in files:
            stdin,stdout,stderr = client.exec_command("cd ~/sprint1; git pull")        
            print '\n'.join(stdout.readlines()), '\n'.join(stderr.readlines())
            print 'repository repulled'
        else:
            stdin,stdout,stderr = client.exec_command("cd ~/; git clone https://github.com/ajhoward7/sprint1.git")        
            print '\n'.join(stdout.readlines()), '\n'.join(stderr.readlines())
            print 'repository created'
    except Exception as e:
        print e

        
def update_crontab(client, prefix):
    print "initializing crontab script for '%s'" % prefix
    msg = '* * * * * python /home/ec2-user/sprint1/json_digest.py'
    try:
        client.exec_command('crontab -r')
        client.exec_command('(crontab -l 2>/dev/null; echo "*/5 * * * * python /home/testtest/sprint1/json_digest.py --prefix %s") | crontab -' % prefix)
        print 'cron tab updated'
    except Exception as e:
        print(e)        


def deploy(key_url, server_url, prefix):
    c = connect(key_url, server_url)
    git_pull(c)
    update_crontab(c, prefix)
    print "script successfully deployed"
    c.close()

