from flask import render_template, redirect, request, session

import sys
sys.path.append('python-sdk/lib')
from meli import Meli

from melinder import app

CLIENT_ID = 1740763944371557
CLIENT_SECRET = "vHgHCql4k59sqIkWfpNqPHedh6lucGEK"
REDIRECT_URI = "http://localhost:5000/authorize"

meli = Meli(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)



@app.route("/login")
def login():
    redirectUrl = meli.auth_url(redirect_URI=REDIRECT_URI)
    return redirect(redirectUrl)


@app.route("/authorize")
def authorize():
	meli.authorize(code=request.args.get('code', ''), redirect_URI=REDIRECT_URI)
	session['access_token'] = meli.access_token
	session['refresh_token'] = meli.refresh_token
	return redirect("/")


@app.route("/")
def index():
	if not 'access_token' in session or not 'refresh_token' in session:
		return redirect("/login")
	meli_auth = Meli(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token=session['access_token'], refresh_token=session['refresh_token'])
	return meli_auth.get("/users/666").content

