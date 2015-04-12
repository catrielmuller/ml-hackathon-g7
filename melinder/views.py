from melinder import app
from flask import send_from_directory, session, current_app
import os
import json

PWD = os.environ.get('PWD')
STATIC_FOLDER = os.path.join(PWD, 'public')


def login_required(func):
    def f(**args):
        if not 'access_token' in session or not 'refresh_token' in session:
            return redirect("/login")
    return f


@login_required
@app.route('/')
def index():
    return send_from_directory(STATIC_FOLDER, "index.html")


@login_required
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(STATIC_FOLDER, path)


@login_required
@app.route('/api/offer/<offer>/change_price/')
def change_price():
    # chequear que <offer> sea de <me>
    # publicar un item igual a <offer>
    # devolver item
    #meli.get("/sites/MLA/search/?category=MLA5725&q=ipod", {'access_token': session['access_token']}).content
    return ""



@login_required
@app.route('/test')
def test():
    current_app.data.insert('like', {'like': 'true'})

    #meli.get("/sites/MLA/search/?category=MLA5725&q=ipod", {'access_token': session['access_token']}).content
    return ""
