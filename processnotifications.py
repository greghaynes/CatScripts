#! /usr/bin/python
from subprocess import Popen, PIPE
import json

class Process(object):
	def __init__(self):
		pass
	def loadFromString(self, line):
		args = line.split(None, 3)
		self.username = args[0]
		self.pid = args[1]
		self.etime = args[2]
		self.command = args[3]
		self.setEtimeFromString(self.etime)
	def setEtimeFromString(self, string):
		args = string.split('-')
		if len(args) == 1:
			self.days = 0
			args = args[0]
		else:
			self.days = int(args[0])
			args = args[1]
		args = args.split(':')
		if len(args) == 2:
			self.hours = 0
			ndx = 0
		else:
			self.hours = int(args[0])
			ndx = 1
		self.mins = int(args[ndx])
		self.secs = int(args[ndx+1])
		self.esecs = (self.days * (24*60*60)) + (self.hours * 60*60) + self.mins*60 + self.secs

pscmd = "ps ak -etime -o user,pid,etime,cmd"
psProc = Popen(pscmd, shell=True, bufsize=4096, stdout=PIPE)
psProc.wait()
buff = psProc.stdout.read()
buff_lines = buff.split("\n")
buff_lines = buff_lines[1:len(buff_lines)-2]

processes = []

for line in buff_lines:
	p = Process()
	p.loadFromString(line)
	processes.append(p)

resp = []
for p in processes:
	resp.append({'pid': p.pid, 'esecs': p.esecs, 'command': p.command, 'username': p.username})

encoder = json.JSONEncoder()
print encoder.encode(resp).decode()
