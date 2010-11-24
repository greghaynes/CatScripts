#!/usr/bin/python
import settings
import commands
import sys

keep_running = True
while keep_running:
	data = ''
	while data.find(settings.command_delim) == -1:
		data += sys.stdin.read(1)
		if len(data) == 0:
			break
	data = data.replace(settings.command_delim, '')
	if data == 'exit':
		keep_running = False
		print 'goodbye'
	else:
		try:
			commands.run_command(data)
		except ValueError:
			print 'invalid_command'
		print settings.response_delim
		sys.stdout.flush()
	
