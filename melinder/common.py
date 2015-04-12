from flask import send_from_directory, current_app, request, session, redirect
import json
import os

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


amazon_api = API(locale='es', access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                 secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                 associate_tag=os.environ.get('AWS_ASSOCIATE_TAG'))


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

                    product_entry = {
                        'product_id': str(product.ASIN),
                        'image_url': str(image_url),
                        'description': unicode(product.ItemAttributes.Title),
                        'category': category['_id']
                    }
                    app.logger.debug('Entry {}'.format(product_entry))
                    current_app.data.insert('product', product_entry)
                except AttributeError:
                    continue

    return ''



@app.route('/load_categories')
@login_required
def load_categories():
    # Borrar las categorias viejas
    #for category in current_app.data.find('category', parse_request('category'), {}):
    #    current_app.data.remove('category', {'_id': str(category['_id'])})
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

