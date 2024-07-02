#!/usr/bin/env python

import pywemo
import schedule
import socket
from flask import Flask
from flask_apscheduler import APScheduler

# flask
app = Flask(__name__)

# scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# wemo device
wemo_url = pywemo.setup_url_for_address(open('wemo_ip', 'r').readlines()[0].strip())
wemo_device = pywemo.discovery.device_from_description(wemo_url)

@app.route('/toggle')
def toggle():
	wemo_device.toggle()
	return ':3'

def netcheck():
	try:
		host = socket.gethostbyname('one.one.one.one')
		sock = socket.create_connection((host, 80), 2)
		sock.close()
	except:
		pass
		print('network probably down')
		toggle()
		time.sleep(10)
		toggle()

scheduler.add_job(id = 'wemo', func = netcheck, trigger = 'interval', seconds = 5)
app.run(host = '0.0.0.0')
