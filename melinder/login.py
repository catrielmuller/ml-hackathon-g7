from flask import render_template, redirect, request, session

import sys
sys.path.append('python-sdk/lib')
from meli import Meli

from melinder import app

CLIENT_ID = 5869207199853659
CLIENT_SECRET = "GnSUwAXDgI6PnkVOFtvujLdMYgOkVeCo"
REDIRECT_URI = "http://localhost:5000/authorize"

meli = Meli(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)


@app.route("/main")
def main():
    return render_template('main.html')


@app.route("/login")
def login():
    redirectUrl = meli.auth_url(redirect_URI=REDIRECT_URI)
    return redirect(redirectUrl)


@app.route("/authorize")
def authorize():
    meli.authorize(code=request.args.get('code', ''), redirect_URI=REDIRECT_URI)
    session['access_token'] = meli.access_token
    return redirect("/")


@app.route("/")
def index():
    if not 'access_token' in session:
        return redirect("/main")
    meli_auth = Meli(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token=session['access_token'])
    return meli_auth.get("/users/666").content


if __name__ == "__main__":
    app.debug = True
    app.secret_key = "\xe6\xd7\xcd2\x16\xb8\xa0,\x10\xb8V\xf8\xed\xa01\x9a\xbe\xfb\xa5\x88\xff\x0e\xd5"
    app.run()


