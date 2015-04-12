from flask import send_from_directory, current_app, request, session, redirect
import json

from eve.utils import parse_request

from melinder import app, STATIC_FOLDER
from login import meli, login_required


@app.route('/api/product/<product_id>/like')
@login_required
def like(product_id):
    product = current_app.data.find("product", parse_request('product'), {'_id': product_id})[0]
    category = current_app.data.find("category", parse_request('category'), {'_id': product['category']})[0]

    items = json.loads(meli.get("/sites/MLA/search/?category=%s&q=%s" % (category['meli_id'], product['description'])).content)
    #items = json.loads(meli.get("/sites/MLA/search/?q=%s" % category['meli_id']).content)

    #current_app.data.insert('like', {'does_like': request.args.get('value'), 'user': session['user_id'], 'product': product_id})

    return json.dumps(items)
