from functools import wraps
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


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'user_id' in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


@app.route("/login")
def login():
    redirectUrl = meli.auth_url(redirect_URI=REDIRECT_URI)
    return redirect(redirectUrl)


@app.route("/logout")
@login_required
def logout():
    if 'access_token' in session: del session['access_token']
    if 'refresh_token' in session: del session['refresh_token']
    if 'meli_id' in session: del session['meli_id']
    if 'meli_email' in session: del session['meli_email']
    if 'user_id' in session: del session['user_id']
    return "Logged out"



@app.route("/app")
@login_required
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


@app.route("/api/me")
@login_required
def me():
    return json.dumps({'id': session['meli_id'], 'email': session['meli_email']})
