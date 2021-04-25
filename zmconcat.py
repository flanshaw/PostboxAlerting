import json, urllib.request
import datetime
from datetime import timedelta
from shutil import copyfile
import glob
import subprocess
import random
import string
import os

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def concatenate(flag):
	# if flag set to 0 create random one time file name
	if flag == 0:
		file_name = randomString()+".mp4"
	else:
		file_name = "output.mp4"
	full_file_name = "/home/playroom/zmvideos/"+file_name
	print("FILENAME...........",file_name)
	stringa = "ffmpeg -i \"concat:"
	elenco_video = glob.glob("/home/playroom/zmvideos/*.mp4")
	elenco_video.sort(key=os.path.getmtime)
	elenco_file_temp = []
	for f in elenco_video:
		file = "/home/playroom/zmvideos/temp" + str(elenco_video.index(f) + 1) + ".ts"
		os.system("ffmpeg -i " + f + " -c copy -bsf:v h264_mp4toannexb -f mpegts " + file)
		elenco_file_temp.append(file)
	#print(elenco_file_temp)
	for f in elenco_file_temp:
		stringa += f
		if elenco_file_temp.index(f) != len(elenco_file_temp)-1:
			stringa += "|"
		else:
			stringa += "\" -c copy  -bsf:a aac_adtstoasc "+ full_file_name
	os.system(stringa)
	print("copying file for hassio:",full_file_name)
	copyfile(full_file_name,"/home/user/docker/hassio/homeassistant/www/"+file_name)
	#logging.info("copied file to /home/user/docker/hassio/homeassistant/www/%s",file)
	return file_name

def new_zmmovie(startdate,starttime,enddate,endtime,random):
	zm_url="http://192.168.0.10/zm/api/events/index/MonitorId:1/StartTime%20%3E=:"+startdate+"%20"+starttime+"/EndTime%20%3C=:"+enddate+"%20"+endtime+".json"
	print(zm_url)
	with urllib.request.urlopen(zm_url) as url: 
		data = json.loads(url.read().decode())
		eventcount=data['pagination']['count']
        #logging.info('event count:%s',eventcount)
		print(eventcount)
		if data['events']:
			for event in data['events']:
				eventid = event['Event']['Id']
				print(eventid)
				eventdate=event['Event']['StartTime'][0:10]
				source_path = "/var/cache/zoneminder/events/1/"+eventdate+"/"+eventid+"/"+eventid+"-video.mp4"
				dest_path = "/home/playroom/zmvideos/"+eventid+".mp4"
				print("source:",source_path," dest:",dest_path)
				try: copyfile(source_path,dest_path)
				except: logging.info("couldn't copy file")
			return concatenate(random)
		else:
			return "noevents"

def cleanfolder():
	files = glob.glob('/home/playroom/zmvideos/*')
	for f in files:
		os.remove(f)

