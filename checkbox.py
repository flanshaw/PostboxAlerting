#!/usr/bin/python3

#runs as checkbox.service in systemctl status checkbox.service
#runs every 30s and checks if ./touch.txt has been touched (postbox open)
#if has, runs zm API, then copies last movie to  hassio/www and sends a message 
# TOUCH.TXT  is touched by the script below
#when postbox open = YES
# SCRIPT IS /home/user/docker/hassio/homeassistant/python_scripts/MOVIE.PY

from zmconcat import new_zmmovie, cleanfolder
from read_latestdhcp import get_latestdhcp

import json, urllib.request
import datetime
from datetime import timedelta
from shutil import copyfile
import time
import os
import logging
import subprocess
from twilio.rest import Client


def send_text(url_link):
    body = {'data': url_link}
    myurl = "https://prod-51.westeurope.logic.azure.com:443/workflows/xxxx/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xxxxxxxx"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    logging.info(".....sending url request")
    try:
        response = urllib.request.urlopen(req, jsondataasbytes)
        logging.info(response)
    except:
        logging.info("ERROR ..couldnt sent")
    return response

def textme(body_txt,number):
    account_sid = 'xxxx'
    auth_token = 'xxxx'
    client = Client(account_sid, auth_token)
    logging.info(".....sending url request, via twilio")
    message = client.messages.create(body= body_txt,from_="xxxxx",to=number)
    pass

logging.basicConfig(filename='/home/playroom/checkbox.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(message)s')
Continue = True
while True:
    touchtime = os.path.getmtime("/home/user/docker/hassio/homeassistant/touch.txt")
    modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(touchtime))
    logging.info('modiciation time=:%s',modificationTime)
    print("mod tine:",modificationTime)
    last_time = (time.time() - touchtime)
    should_time = time.time() - (30)
    if touchtime > should_time :
        logging.info("recently updated...create movie")
        print("creating movie...")
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        end_time = datetime.datetime.now().strftime('%H:%M:%S')
        start_date = (datetime.datetime.now() - timedelta(minutes = 15)).strftime('%Y-%m-%d')
        start_time = (datetime.datetime.now() - timedelta(minutes = 15)).strftime('%H:%M:%S')
        logging.info("running new_zmovie %s %s",end_time,start_time)
        print("running new_zmovie:",end_time,"....",start_time)
        file_name = new_zmmovie(start_date,start_time,end_date,end_time,0)
        cleanfolder()
        print("...........sending text:http://"+get_latestdhcp()+":8123/local/",file_name)
        print("...........sending text:http://"+get_latestdhcp()+":8123/local/",file_name)
        #send_text("http://"+get_latestdhcp()+":8123/local/"+file_name)
        smstext = "your postbox as been opened " + "http://"+get_latestdhcp()+":8123/local/"+file_name
        textme(smstext,"+447912775261") 
        textme(smstext,"+447754089900")
        mutt_cmd= 'echo http://'+ get_latestdhcp()+':8123/local/' + file_name + ' | mutt -s "postbox video" xxxxx@gmail.com'
        a = subprocess.Popen(mutt_cmd, shell=True)
        #cleanfiles
        #send text message with link to file
        #createmovie()
    logging.info("sleeping for 30s")
    print("sleeping...........")
    time.sleep(30)





