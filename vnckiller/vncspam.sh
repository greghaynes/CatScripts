#! /bin/bash

# Processes running this many hours or more will be spammed
SPAMEHRS=12
ALERT_MESSAGE="Your session will be killed in $SPAMEHRS hours."

ETIME_REGEX="([0-9][0-9]*-[0-9][0-9]:[0-9][0-9]:[0-9][0-9]|[$SPAMEHRS-23]:[0-9][0-9]:[0-9][0-9])"
PROCESS_REGEX="Xvnc"

DISPLAYS=$(ps -eo etime,pid,user,args | grep $PROCESS_REGEX | awk "/$ETIME_REGEX/ {print \$5}")

for DISP in $DISPLAYS
do
	echo "export DISPLAY=$DISP"
	echo "/usr/local/X11/bin/xmessage $ALERT_MESSAGE"
done

