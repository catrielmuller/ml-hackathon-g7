from melinder import app
from flask import send_from_directory, session
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

