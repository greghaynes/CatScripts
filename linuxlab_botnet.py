#! /usr/bin/python
from subprocess import Popen, PIPE
import json
import sys
import procviewer

import settings

hosts_cmd = '/cat/bin/netgrouplist linux-linuxlab-sys'
#hosts_cmd = 'echo african.cs.pdx.edu'
ssh_cmd = '/usr/bin/ssh %s ./scripts/commandlistener.py'

hostsProc = Popen(hosts_cmd, shell=True, bufsize=4096, stdout=PIPE)
hostsProc.wait()
buff = hostsProc.stdout.read()
buff_lines = buff.split('\n')
buff_lines = buff_lines[:len(buff_lines)-1]

ssh_procs = []
for line in buff_lines:
	cur_ssh_proc = Popen(['/usr/bin/ssh', line, './scripts/commandlistener.py'], stdin=PIPE, stdout=PIPE)
	ssh_procs.append((line, cur_ssh_proc))

def process_summary_view(host_process):
	procviewer.view_json_host_procs(host_process)

cmd_response_processors = {
	'process_summary': process_summary_view,
}

keep_running = True
while keep_running:
	cmd = raw_input(">")
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
		try:
			cmd_response_processors[cmd](responses)
		except KeyError:
			print 'Command not found'

