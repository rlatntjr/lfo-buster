###
#
# Interface required
# 
# Target EID
#   or
# Target User ID
#
# For each user ID:
#   For each folder/file to move:
#     Folder/File ID, Path, isDeleted?
#
#
#
# Checklist:
# - simple move from root
# - simple move from path

from boxsdk import OAuth2, Client
from flask import Flask, abort, request

import urllib
import webbrowser
import socket
import csv

holding_user = 1024329

app = Flask(__name__)

oauth = OAuth2(
	client_id='75dq6aw0k3ngrw32tfza0bhtzekmj5xr',
	client_secret='IhcYvwiKFQsJjyPW7iHs0b8m6iXyHbGx'
)

auth_url, csrf_token = oauth.get_authorization_url('http://localhost:8888/')
state, code = None, None

webbrowser.open(auth_url)

@app.route('/')
def callback():
	state, code = request.args.get('state', ''), request.args.get('code', '')
	assert state == csrf_token
	access_token, refresh_token = oauth.authenticate(code)
	# client = Client(oauth)

	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()

if __name__ == '__main__':
	app.run(port = 8888)

client = Client(oauth)

with open('input.csv', 'rU') as f:
	reader = csv.reader(f)
	for row in reader:
		print row