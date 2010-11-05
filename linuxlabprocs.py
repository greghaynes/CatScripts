#! /usr/bin/python
from subprocess import Popen, PIPE
import json

hosts_cmd = 'netgrouplist linux-linuxlab-sys'
ssh_cmd = 'ssh %s ./scripts/processnotifications.py'

hostsProc = Popen(hosts_cmd, shell=True, bufsize=4096, stdout=PIPE)
hostsProc.wait()
buff = hostsProc.stdout.read()
buff_lines = buff.split('\n')
buff_lines = buff_lines[:len(buff_lines)-1]

host_procs = []
for line in buff_lines:
	sshProc = Popen(ssh_cmd % line, shell=True, bufsize=4096, stdout=PIPE)
	sshProc.wait() 
	host_procs.append({'host': line, 'processes': json.load(sshProc.stdout)})

print json.dumps(host_procs).decode()
