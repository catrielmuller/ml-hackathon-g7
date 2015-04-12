from amazonproduct import API
from eve.utils import parse_request

from melinder import app
from login import meli, login_required

from flask import send_from_directory, current_app
import os
import json


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
            product_entry = {''}


@login_required
@app.route('/api/offer/<offer>/change_price/')
def change_price():
    # chequear que <offer> sea de <me>
    # publicar un item igual a <offer>
    # devolver item
    #meli.get("/sites/MLA/search/?category=MLA5725&q=ipod", {'access_token': session['access_token']}).content
    return ""



@login_required
@app.route('/api/product/<product_id>/like')
def like(product_id):
    current_app.data.insert('like', {'does_like': request.get('value'), 'user': request['user_id'], 'product': product_id})
    product = current_app.data.find("product", {'_id': like.product})
    category = current_app.data.find("category", {'_id': product.category})

    items = json.loads(meli.get("/sites/MLA/search/?category=%s&q=%s" % (category.meli_id, product.description)).content)

    return items


@login_required
@app.route('/load_categories')
def load_categories():
    categories = json.loads(meli.get("/sites/MLA/categories").content)
    return json.dumps(categories)
    for category in categories:
        current_app.data.insert('category', {
            'meli_id': category['id'], 
            'name': category['name']
        })
    return categories

