from paramiko import *
from scp import SCPClient
import paramiko


'''
SCP command is as following.
scp wipro-dev-nestle_wipro-dev-nestle_20161216-144742_dump.tar.bz2 nirav.joshi@108.168.207.6:/home/nirav.joshi/
'''
def createSSHClient(server, port, user,password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user,password)
    return client

ssh = createSSHClient('108.168.207.6',22,'nirav.joshi','S9vDYtYn')
scp = SCPClient(ssh.get_transport())
ssh = createSSHClient('108.168.207.6',22,'nirav.joshi','S9vDYtYn')

scp.put("/Users/nirav/logs/saas-prodcm71-wk/saas-prodcm71-wk-app99/wipro-prod-nestle-app02_access_log_2016-12-09.bz2")
