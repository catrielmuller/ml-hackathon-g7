from flask import current_app, request, session, redirect
import json
import random

from eve.utils import parse_request

from melinder import app
from login import meli, login_required


@app.route('/api/product/<product_id>/like')
@login_required
def like(product_id):
    current_app.data.insert('like', {'does_like': request.args.get('value'), 'user': session['user_id'], 'product': product_id})
    product = current_app.data.find("product", parse_request('product'), {'_id': like.product})
    category = current_app.data.find("category", parse_request('category'), {'_id': product.category})

    items = json.loads(meli.get("/sites/MLA/search/?category=%s&q=%s" % (category.meli_id, product.description)).content)

    return items


@app.route('/api/suggest_products')
@login_required
def suggest_products():
    user = current_app.data.find('user', parse_request('user'), {'_id': session['user_id']})[0]

    items_cursor = current_app.data.find('product', parse_request('product'), {'category': {'$in': user['preferences']}})
    items = []
    if items_cursor.count() > 0:
        items = [item for item in items_cursor]
        items = random.shuffle(items)

    return json.dumps(items)

