from flask import render_template, redirect, request, session
from eve import methods as api
import json
import requests

import sys
sys.path.append('meli/lib')
from meli import Meli

from melinder import app
from settings import API

CLIENT_ID = 1740763944371557
CLIENT_SECRET = "vHgHCql4k59sqIkWfpNqPHedh6lucGEK"
#REDIRECT_URI = "http://3b38f96a.ngrok.com/authorize"
REDIRECT_URI = "http://localhost:5000/authorize"

meli = Meli(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)



@app.route("/login")
def login():
    redirectUrl = meli.auth_url(redirect_URI=REDIRECT_URI)
    return redirect(redirectUrl)


@app.route("/authorize")
def authorize():
	if request.method == 'GET':
		meli.authorize(code=request.args.get('code', ''), redirect_URI=REDIRECT_URI)

		user = json.loads(meli.get("/users/me", {'access_token': session['access_token']}).content)
		exists = api.get('user', {'where': '{"meli_id": "%d"}' % user['id']})[0]['_items']
		if not exists:
			#return API + "user/?" +  json.dumps({"meli_id": str(user['id']), "email": user['email']})
			response = requests.post('http://localhost:5000/api/user', json={'meli_id': '1', 'email': 'diegolis@gmail.com'}, headers={'Content-Type': 'application/json'})
			print response
			#requests.post(API + "user/", json=json.dumps({"meli_id": str(user['id']), "email": user['email']}), headers={"Content-Type": "application/json"})
			assert False
			#api.put('user', {"meli_id": user['id'], "email": user['email']}, headers={"Content-Type": "application/json"})


		session['access_token'] = meli.access_token
		session['refresh_token'] = meli.refresh_token
		return redirect("/")


@app.route("/")
def index():
	if not 'access_token' in session or not 'refresh_token' in session:
		return redirect("/login")
	return redirect("/index.html")

