from flask import render_template, redirect, request, session, current_app
from eve import methods as api
from eve.utils import parse_request
import json
import requests

import sys
sys.path.append('meli/lib')
from meli import Meli

from melinder import app
from settings import API

CLIENT_ID = 1740763944371557
CLIENT_SECRET = "vHgHCql4k59sqIkWfpNqPHedh6lucGEK"
REDIRECT_URI = "http://localhost:5000/authorize"

meli = Meli(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)


def login_required(func):
    def f(**args):
        if not 'access_token' in session or not 'refresh_token' in session:
            return redirect("/login")
    return f


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

    user = json.loads(meli.get("/users/me", {'access_token': session['access_token']}).content)
    exists = current_app.data.find('user', parse_request('user'), {"meli_id": user['id']})
    if exists.count() == 0:
        current_app.data.insert('user', {'meli_id': user['id'], 'email': user['email']})

    return redirect("/")


@app.route("/api/me")
def me():
    user = meli.get("/users/me", {'access_token': session['access_token']}).content
    return user
