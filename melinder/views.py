from amazonproduct import API
from eve.utils import parse_request

from melinder import app
from login import login_required
from flask import send_from_directory, current_app
import os


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
            exists = current_app.data.find('product', parse_request('product'), {'product_id': product.ASIN})
            if not exists:
                image_url = amazon_api.item_lookup(product.ASIN, ResponseGroup='Images').Item.LargeImage.URL
                product_entry = {'product_id': product.ASIN, 'image_url': image_url, 'description': product.Title,
                                 'category': category['_id']}
                current_app.data.insert('product', product_entry)


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
