import json, urllib.request
import datetime
from datetime import timedelta
from shutil import copyfile
import time
import os
#27.3.2021
#this is the python run from home assistant automation
#when postbox open = YES
#/home/user/docker/hassio/homeassistant/python_scripts

if os.path.exists("touch.txt"):
	os.utime("touch.txt",None)
else: 
	open("touch.txt",'a').close()
print("sleeping for 120s..")
time.sleep(120)

