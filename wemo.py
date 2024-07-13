#!/usr/bin/env python

import pywemo
import schedule
import socket
import time
from datetime import datetime
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
	print('// toggled wemo :3')
	return ':3'

def checkHost(hostname):
	try:
		host = socket.gethostbyname(hostname)
		sock = socket.create_connection((host, 80), 15)
		sock.close()
		print(f'++ {hostname} ({host})')
		return True
	except:
		pass
		print(f'-- {hostname}')
		return False

def netcheck():
	print(f'// {datetime.now()}')

	# list of hosts to check
	HOSTS = ['one.one.one.one', 'www.google.com', 'www.example.org']

	# threshold of hosts that need to be online
	THRESHOLD = 2

	# check each host
	failed = 0
	for host in HOSTS:
		if not checkHost(host): failed += 1

	if failed >= THRESHOLD:
		print('!! network possibly down :c')

		# turn off modem for 15 seconds
		toggle()
		time.sleep(15)

		# turn on modem and pause for 5 minutes to allow bootup
		toggle()
		time.sleep(60 * 5)
	else:
		print('// all good :3')
	print('')

scheduler.add_job(id = 'netcheck', func = netcheck, trigger = 'interval', seconds = 30)
app.run(host = '0.0.0.0')
