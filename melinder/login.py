import json
import os
import sys

sys.path.append('meli/lib')

from eve.utils import parse_request
from flask import redirect, request, session, current_app, send_from_directory
from meli import Meli

from melinder import app, STATIC_FOLDER


CLIENT_ID = os.environ.get('MELI_CLIENT_ID', 1740763944371557)
CLIENT_SECRET = os.environ.get('MELI_CLIENT_SECRET', "vHgHCql4k59sqIkWfpNqPHedh6lucGEK")
REDIRECT_URI = os.environ.get('MELI_REDIRECT_URI', "http://localhost:5000/authorize")

meli = Meli(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)


def login_required(func):
    def f(*args, **kwargs):
        if not 'access_token' in session or not 'refresh_token' in session or not 'meli_id' in session:
            return redirect("/login")
        return func(*args, **kwargs)
    return f


@app.route("/login")
def login():
    redirectUrl = meli.auth_url(redirect_URI=REDIRECT_URI)
    return redirect(redirectUrl)


@login_required
@app.route("/app")
def app_begin():
    return send_from_directory(STATIC_FOLDER, 'app.html')


@app.route("/authorize")
def authorize():
    if request.method == 'GET':
        meli.authorize(code=request.args.get('code', ''), redirect_URI=REDIRECT_URI)

    session['access_token'] = meli.access_token
    session['refresh_token'] = meli.refresh_token

    meli_user = json.loads(meli.get("/users/me", {'access_token': session['access_token']}).content)
    session['meli_email'] = meli_user['email']
    session['meli_id'] = meli_user['id']

    exists = current_app.data.find('user', parse_request('user'), {"meli_id": meli_user['id']})
    if exists.count() == 0:
        user_id = str(current_app.data.insert('user', {'meli_id': meli_user['id'], 'email': meli_user['email']}))
    else:
        user_id = exists[0]['_id']

    session['user_id'] = str(user_id)

    return redirect("/app")


@login_required
@app.route("/api/me")
def me():
    if not 'access_token' in session or not 'refresh_token' in session or not 'meli_id' in session:
        return redirect("/login")
    return json.dumps({'id': session['meli_id'], 'email': session['meli_email']})
