import os

from amazonproduct import API
from eve.utils import parse_request
from flask import send_from_directory, current_app

from melinder import app
from melinder.login import login_required

PWD = os.environ.get('PWD')
STATIC_FOLDER = os.path.join(PWD, 'public')

amazon_api = API(locale='es')


@login_required
@app.route('/')
def index():
    return send_from_directory(STATIC_FOLDER, "index.html")


@login_required
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(STATIC_FOLDER, path)


@app.route('/update_amazon_products')
def update_amazon_products():
    categories = current_app.data.find('category', parse_request('category'))[0]

    for category in categories:
        for product in amazon_api.item_search(category['amazon_name'], Keywords=category['name']):
            pass
