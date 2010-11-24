#! /usr/bin/python
from subprocess import Popen, PIPE
import json
import sys
import socket
import os

import procviewer
import settings

# Create control socket
try:
	os.remove(settings.cc_socket_bind)
except OSError:
	pass
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.bind(settings.cc_socket_bind)
s.listen(1)

#hosts_cmd = '/cat/bin/netgrouplist linux-linuxlab-sys'
hosts_cmd = 'echo african.cs.pdx.edu'

hostsProc = Popen(hosts_cmd, shell=True, bufsize=4096, stdout=PIPE)
hostsProc.wait()
buff = hostsProc.stdout.read()
buff_lines = buff.split('\n')
buff_lines = buff_lines[:len(buff_lines)-1]

# initialize ssh connections
ssh_procs = []
for line in buff_lines:
	cur_ssh_proc = Popen(['/usr/bin/ssh', line, './scripts/commandlistener.py'], stdin=PIPE, stdout=PIPE)
	ssh_procs.append((line, cur_ssh_proc))

# main event loop
keep_running = True
while keep_running:
	conn, addr = s.accept()
	# Get a command
	data = ''
	while data.find(settings.cc_command_delim) == -1:
		data += conn.recv(1)
		if len(data) == 0:
			break
	cmd = data.replace(settings.cc_command_delim, '')
	
	# Run command on all bots
	responses = {}
	for hostname, proc in ssh_procs:
		raw_cmd = cmd + settings.command_delim
		proc.stdin.write(raw_cmd)
		proc.stdin.flush()
		resp = ''
		while -1 == resp.find(settings.response_delim):
			resp += proc.stdout.readline()
		resp = resp.replace(settings.response_delim, '')
		resp = json.loads(resp)
		responses[hostname] = resp

	if cmd == 'exit':
		keep_running = False
	else:
		conn.send(json.dumps(responses))
		conn.send(settings.cc_response_delim)
	conn.close()

