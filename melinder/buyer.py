from flask import current_app, request, session, redirect
import json
import random

from eve.utils import parse_request

from melinder import app
from login import meli, login_required


@app.route('/api/suggest_products')
@login_required
def suggest_products():
    user = current_app.data.find('user', parse_request('user'), {'_id': session['user_id']})[0]

    items_cursor = current_app.data.find('product', parse_request('product'), {})
    items = []
    for item in items_cursor:
        #if str(item['category']) in [str(p) for p in user['preferences']]:
        item['_id'] = str(item['_id'])
        item['category'] = str(item['category'])
        items.append(item)
    random.shuffle(items)

    return json.dumps(items)


@app.route('/api/product/<product_id>/like')
@login_required
def like(product_id):
    product = current_app.data.find("product", parse_request('product'), {'_id': product_id})[0]
    category = current_app.data.find("category", parse_request('category'), {'_id': product['category']})[0]

    current_app.data.insert('like', {'does_like': request.args.get('value', 'true').lower() == 'true',
                                     'user': session['user_id'], 'product': product_id, 'viewed': False})

    items = json.loads(meli.get("/sites/MLA/search/?category=%s&q=%s" % (category['meli_id'], product['description'])).content)

    for item in items['results']:
        offer = {
            'meli_seller': item['seller']['id'], 
            'meli_item_id': item['id'], 
            'meli_link': item['permalink'], 
            'meli_image': item['thumbnail'], 
            'product': product_id,
            'original_price': item['price'],
            'new_price': None
        }
        current_app.data.insert('offer', offer)
    return ""


@app.route('/api/get_offers/')
@login_required
def get_offers():
    res = []

    likes = current_app.data.find('like', parse_request('like'), {})
    for l in likes:
        if session['user_id'] == str(l['user']):
            offers = current_app.data.find('offer', parse_request('offer'), {})
            os = [o for o in offers if str(o['product']) == str(l['product'])]
            avg = sum([o['original_price'] for o in os]) / (1.0 * offers.count())
            os = sorted(os, key=lambda x: x['original_price'])
            least = os[0]
            least['avg'] = avg
            least['percent_discount'] = 100*max((avg - least['original_price']) / (1.0 * avg), 0)
            least['product'] = str(least['product'])
            least['_id'] = str(least['_id'])

            res.append(least)

    return json.dumps(res)
