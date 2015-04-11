from flask import render_template, redirect, request, session

import sys
sys.path.append('meli/lib')
from meli import Meli

from melinder import app

CLIENT_ID = 1740763944371557
CLIENT_SECRET = "vHgHCql4k59sqIkWfpNqPHedh6lucGEK"
REDIRECT_URI = "http://3b38f96a.ngrok.com/authorize"

meli = Meli(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)



@app.route("/login")
def login():
    redirectUrl = meli.auth_url(redirect_URI=REDIRECT_URI)
    return redirect(redirectUrl)


@app.route("/authorize")
def authorize():
	if request.method == 'GET':
		meli.authorize(code=request.args.get('code', ''), redirect_URI=REDIRECT_URI)

		session['access_token'] = meli.access_token
		session['refresh_token'] = meli.refresh_token
		return redirect("/")


@app.route("/")
def index():
	if not 'access_token' in session or not 'refresh_token' in session:
		return redirect("/login")
	return meli.get("/users/me", {'access_token': session['access_token']})	.content

