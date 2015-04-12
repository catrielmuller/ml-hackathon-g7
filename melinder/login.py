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

import os

CLIENT_ID = os.environ.get('MELI_CLIENT_ID', 1740763944371557)
CLIENT_SECRET = os.environ.get('MELI_CLIENT_SECRET', "vHgHCql4k59sqIkWfpNqPHedh6lucGEK")
REDIRECT_URI = os.environ.get('MELI_REDIRECT_URI', "http://localhost:5000/authorize")

meli = Meli(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)


def login_required(func):
    def f(**args):
        if not 'access_token' in session or not 'refresh_token' in session or not 'meli_user' in session:
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

    session['meli_user'] = user

    exists = current_app.data.find('user', parse_request('user'), {"meli_id": user['id']})
    if exists.count() == 0:
        user = current_app.data.insert('user', {'meli_id': user['id'], 'email': user['email']})
    else:
    	user = exists[0]

    session['user_id'] = user._id

    return redirect("/")


@login_required
@app.route("/api/me")
def me():
    return session['meli_user']
