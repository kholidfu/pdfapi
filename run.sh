#!/bin/bash
cd $1
source bin/activate
nohup `uwsgi uwsgi.ini` > /dev/null 2>&1 < /dev/null & disown
