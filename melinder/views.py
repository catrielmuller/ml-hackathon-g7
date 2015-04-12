from flask import send_from_directory, current_app, request, session
import json

from amazonproduct import API
from eve.utils import parse_request

from melinder import app, STATIC_FOLDER
from login import meli, login_required


MELI_TO_AMAZON = {
    'Autos, Motos y Otros': 'Automotive', 'Bebes': 'Baby', 'Computaci\\u00f3n': 'Computers',
    'Consolas y Videojuegos': 'VideoGames', 'Deportes y Fitness': 'SportingGoods',
    'Electr\\u00f3nica, Audio y Video': 'Electronics', 'Industrias y Oficinas': 'OfficeProducts',
    'Instrumentos Musicales': 'MusicalInstruments', 'Joyas y Relojes': 'Jewelry',
    'Juegos y Juguetes': 'Toys', 'Libros, Revistas y Comics': 'Books',
    'M\\u00fasica, Pel\\u00edculas y Series': 'DVD', 'Ropa y Accesorios': 'Apparel',
    'Salud y Belleza': 'HealthPersonalCare'
}

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
                product_entry = {
                    'product_id': product.ASIN,
                    'image_url': image_url,
                    'description': product.Title,
                    'category': category['_id']
                }
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
@app.route('/api/product/<product_id>/like')
def like(product_id):
    current_app.data.insert('like', {'does_like': request.args.get('value'), 'user': session['user_id'], 'product': product_id})
    product = current_app.data.find("product", parse_request('product'), {'_id': like.product})
    category = current_app.data.find("category", parse_request('category'), {'_id': product.category})

    items = json.loads(meli.get("/sites/MLA/search/?category=%s&q=%s" % (category.meli_id, product.description)).content)

    return items


@login_required
@app.route('/load_categories')
def load_categories():
    categories = json.loads(meli.get("/sites/MLA/categories").content)
    for category in categories:
        if category['name'] in MELI_TO_AMAZON:
            exists = current_app.data.find("category", parse_request('category'), {'name': category['name']})
            if not exists:
                category_entry = {
                    'name': category['name'],
                    'meli_id': category['id'],
                    'amazon_name': MELI_TO_AMAZON.get(category['name'])
                }
                current_app.data.insert('category', category_entry)

    return json.dumps(categories)

