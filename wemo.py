#!/usr/bin/env python

import json
import pywemo
from flask import Flask

app = Flask(__name__)

@app.route('/toggle')
def toggle():
	url = pywemo.setup_url_for_address(open("wemo_ip", "r").readlines()[0].strip())
	device = pywemo.discovery.device_from_description(url)
	device.toggle()
	return json.dumps({'toggled': True})

@app.route('/')
def index():
	return "hi";

app.run()