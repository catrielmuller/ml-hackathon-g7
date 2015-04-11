from melinder import app
from flask import send_from_directory
import os

PWD = os.environ.get('PWD')
STATIC_FOLDER = os.path.join(PWD, 'public')

#@app.route('/')
#def root():
#    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(STATIC_FOLDER, path)
