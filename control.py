import os
import sys
import socket
import getopt

import settings

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(settings.cc_socket_bind)
s.send(sys.argv[1] + settings.cc_command_delim)
resp = ''
while -1 == resp.find(settings.cc_response_delim):
	resp += s.recv(1)

print resp.replace(settings.cc_response_delim, "")

