#!/bin/bash

source /home/pi/Desktop/barbot/venv/bin/activate

cd /home/pi/Desktop/barbot

sleep 10s 

flask run -h *localip* &  #ip should be static if you host like this


# run.sh --> run.py --> __init__.py
