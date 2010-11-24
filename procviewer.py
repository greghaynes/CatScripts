#! /usr/bin/python

import sys
import getopt
import json

sort_options =  (
	'elapsed',
	'cpu',
	'username',
)

def usage():
	print '%s -p [processfile]' % sys.argv[0]

def sort_elapsed(processes):
	sorted = []
	while len(processes) > 0:
		best = processes[0]
		best_i = 0
		i = 0
		for proc in processes:
			if proc['esecs'] > best['esecs']:
				best = proc
				best_i = i
			i += 1
		sorted.append(best)
		del processes[best_i]
	return sorted

def strip_root_procs(processes):
	ret = []
	for proc in processes:
		if proc['username'] != 'root':
			ret.append(proc)
	return ret

def view_json_host_procs(host_procs_list):
	processes = []
	for host, procs in host_procs_list.items():
		for proc in procs:
			proc['host'] = host
			processes.append(proc)

	processes = sort_elapsed(processes)
	processes = strip_root_procs(processes)
	processes = processes[0:20]

	for proc in processes:
		print proc['host'], proc['pid'], proc['username'], proc['command'], proc['esecs']

def main(argv):
	procfile = None
	sort_method = 'elapsed'
	show_root = False

	try:
		opts, args = getopt.getopt(argv, "hrp:s:", ["help", "processfile"])
	except getopt.GetOptError:
		usage()
		sys.exit(2)

	for o, a in opts:
		if o in ('-h', '--help'):
			usage()
			sys.exit(2)
		elif o in ('-p', '--processfile'):
			procfile = a

	if procfile == None:
		print "Error: No process file specified"
		usage()
		sys.exit(2)
	
	decoder = json.JSONDecoder()
	procf = open(procfile)
	buff = procf.read()
	host_procs_list = decoder.decode(buff)
	processes = []


if __name__ == "__main__":
	main(sys.argv[1:])
