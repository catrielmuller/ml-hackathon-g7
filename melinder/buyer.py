from flask import send_from_directory, current_app, request, session, redirect
import json

from eve.utils import parse_request

from melinder import app, STATIC_FOLDER
from login import meli, login_required


@app.route('/api/product/<product_id>/likes')
@login_required
def likes(product_id):
    product = current_app.data.find("product", parse_request('product'), {'_id': product_id})[0]
    category = current_app.data.find("category", parse_request('category'), {'_id': product['category']})[0]

    does_like = request.args.get('value').lower() == 'true'
    current_app.data.insert('like', {'does_like': does_like, 'user': session['user_id'], 'product': product_id})

    #items = json.loads(meli.get("/sites/MLA/search/?q=%s" % product['description']).content)
    items = json.loads(meli.get("/sites/MLA/search/?category=%s&q=%s" % (category['meli_id'], product['description'])).content)
    for item in items:
        offer = {
            'meli_seller': item['seller']['id'], 
            'meli_item_id': item['id'], 
            'meli_link': item['permalink'], 
            'meli_image': item['thumbnail'], 
            'product': product_id,
            'original_price': item['price'],
            'new_price': None,
            'viewed': False,
            }
        current_app.data.insert('offer', offer)
    return ""


@app.route('/api/product/<product_id>/like')
@login_required
def like(product_id):
    product = current_app.data.find("product", parse_request('product'), {'_id': product_id})[0]
    category = current_app.data.find("category", parse_request('category'), {'_id': product['category']})[0]

    current_app.data.insert('like', {'does_like': request.args.get('value'), 'user': session['user_id'], 'product': product_id})

    #items = json.loads(meli.get("/sites/MLA/search/?q=%s" % product['description']).content)
    items = json.loads(meli.get("/sites/MLA/search/?category=%s&q=%s" % (category['meli_id'], product['description'])).content)
    for item in items:
        offer = {
            'meli_seller': item['seller']['id'], 
            'meli_item_id': item['id'], 
            'meli_link': item['permalink'], 
            'meli_image': item['thumbnail'], 
            'product': product_id,
            'original_price': item['price'],
            'new_price': None,
            'viewed': False,
            }
        current_app.data.insert('offer', offer)
    return ""


