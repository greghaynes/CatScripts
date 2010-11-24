import processmanager
import sys

cmd_table = {
	'process_summary': processmanager.summary
	}

def run_command(cmd):
	exit
	try:
		cmd_table[cmd]()
	except KeyError:
		raise ValueError('Invalid Command')

