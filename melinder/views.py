from flask import send_from_directory, current_app, request, session, redirect
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


@app.route('/')
@login_required
def index():
    return send_from_directory(STATIC_FOLDER, "index.html")


@app.route('/<path:path>')
@login_required
def static_proxy(path):
    return send_from_directory(STATIC_FOLDER, path)


@app.route('/update_amazon_products')
@login_required
def update_amazon_products():
    categories = current_app.data.find('category', parse_request('category'), {})
    app.logger.debug('Categories {}'.format(categories))
    for category in categories:
        app.logger.debug('Category {}'.format(category))
        for product in amazon_api.item_search(category['amazon_name'], Keywords=category['name']):
            app.logger.debug('Product ASIN {}'.format(product.ASIN))
            exists = current_app.data.find('product', parse_request('product'), {'product_id': str(product.ASIN)}).count() > 0
            if not exists:
                try:
                    image_url = amazon_api.item_lookup(str(product.ASIN), ResponseGroup='Images').Items.Item.LargeImage.URL
                except AttributeError:
                    image_url = amazon_api.item_lookup(str(product.ASIN), ResponseGroup='Images').Items.Item.URL

                product_entry = {
                    'product_id': str(product.ASIN),
                    'image_url': str(image_url),
                    'description': unicode(product.ItemAttributes.Title),
                    'category': category['_id']
                }
                app.logger.debug('Entry {}'.format(product_entry))
                current_app.data.insert('product', product_entry)

    return ''


@app.route('/api/offer/<offer>/change_price/')
@login_required
def change_price():
    # chequear que <offer> sea de <me>
    # publicar un item igual a <offer>
    # devolver item
    #meli.get("/sites/MLA/search/?category=MLA5725&q=ipod", {'access_token': session['access_token']}).content
    return ""


@app.route('/api/product/<product_id>/like')
@login_required
def like(product_id):
    current_app.data.insert('like', {'does_like': request.args.get('value'), 'user': session['user_id'], 'product': product_id})
    product = current_app.data.find("product", parse_request('product'), {'_id': like.product})
    category = current_app.data.find("category", parse_request('category'), {'_id': product.category})

    items = json.loads(meli.get("/sites/MLA/search/?category=%s&q=%s" % (category.meli_id, product.description)).content)

    return items


@app.route('/load_categories')
@login_required
def load_categories():
    categories = json.loads(meli.get("/sites/MLA/categories").content)
    for category in categories:
        if category['name'] in MELI_TO_AMAZON:
            exists = current_app.data.find("category", parse_request('category'), {'name': category['name']})
            if exists.count() == 0:
                category_entry = {
                    'name': category['name'],
                    'meli_id': category['id'],
                    'amazon_name': MELI_TO_AMAZON.get(category['name'])
                }
                current_app.data.insert('category', category_entry)

    return json.dumps(categories)

