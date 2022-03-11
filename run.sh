#!/bin/bash

source /home/pi/Desktop/barbot/venv/bin/activate

cd /home/pi/Desktop/barbot

sleep 10s 

flask run -h 192.168.178.52 & #hier muss die ip vom pi stehen, am besten sollte diese statisch sein  


#es läuft run.sh --> run.py --> __init__.py
