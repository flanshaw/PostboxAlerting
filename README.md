I wanted to be sent a video everytime someone put something into the postbox. ive a cctv camera watching the drive, which detects the motion, but this detects ALL motion.
I'll post links here to where i got the inspiration from. 

# Postbox Alerting
Combination of custom ESP8266 PCB, powered by 18650, mqtt and few python scrips and homeassistant that sends text message with link to video  (zoneminder) if my postbox is opened

# PCB
PCB to fit an esp8266, powered by one 18650. Reed switch and magnet duck taped to the postbox lid. When postboxed is opened, it opens a circuit to the battery, which powers esp8266, and switches on a transistors to maintain power once lid is closed.

# ESP8266 Code
sends "OPEN" paylod to cloud hosted mqtt server on topic /tele/postbox

# hassio 
hassio (run in docker container) subscribes to /tele/postbox and automation is triggered on an OPEN message, it 'touches' a loal touch.txt file

# checkbox.py
checkbox.py runs as a ubuntu service and monitors touch.txt, to see if it has changed, and if it has sends text message with link to MP4 url accessible via hassio
