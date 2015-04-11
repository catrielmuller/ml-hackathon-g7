from eve import Eve
from flask import send_from_directory
import os
import pymongo

from components import users

EVE_SETTINGS = {
    'DOMAIN': {},
    'URL_PREFIX': 'api',
    'MONGO_DBNAME': 'melinder',
    'XML': False,
    'HATEOAS': False,
    'IF_MATCH': False,
    'BANDWIDTH_SAVER': False,
    'MONGO_QUERY_BLACKLIST': ['$WHERE'],
    'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
    'ITEM_METHODS': ['GET', 'PUT', 'DELETE'],
    'PAGINATION_LIMIT': 10000
}


PWD = os.environ.get('PWD')
STATIC_FOLDER = os.path.join(PWD, 'public')

app = Eve(settings=EVE_SETTINGS, static_folder=STATIC_FOLDER)


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(STATIC_FOLDER, path)


def initialize_components(eve_app, components):
    """Initialize components' resources with the Eve app.  Accepts a single item or a list of them.  Each item must be
    a package with a variable called RESOURCES, which is a list of dictionaries, each containing the configuration
    information for a resource."""
    components = components if isinstance(components, (list, tuple)) else [components]
    for component in components:
        for resource in component.RESOURCES:
            _initialize_resource(eve_app, resource)


def _initialize_resource(eve_app, resource):
    """Register a resource and its event callbacks with the Eve app (after initializing any components the resource
    depends on)"""
    name = resource['name']
    if name not in eve_app.config['DOMAIN']:
        initialize_components(eve_app, resource.get('dependencies', []))
        eve_app.register_resource(name, resource['domain_settings'])
        _ensure_indexes(name, resource.get('indexes', []))


def _ensure_indexes(resource_name, indexes):
    client = pymongo.MongoClient()
    db = client[EVE_SETTINGS['MONGO_DBNAME']]
    for index, options in indexes:
        db[resource_name].ensure_index(index, **options)


initialize_components(app, [users])


if __name__ == '__main__':
    app.run()
