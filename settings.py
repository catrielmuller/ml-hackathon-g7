import os

EVE_SETTINGS = {
    'DOMAIN': {},
    'URL_PREFIX': 'api',
    'XML': False,
    'HATEOAS': False,
    'IF_MATCH': False,
    'BANDWIDTH_SAVER': False,
    'MONGO_QUERY_BLACKLIST': ['$WHERE'],
    'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
    'ITEM_METHODS': ['GET', 'PUT', 'DELETE'],
    'PAGINATION_LIMIT': 10000
}


if os.environ.get('PORT'):
    EVE_SETTINGS['MONGO_HOST'] = 'ds061671.mongolab.com'
    EVE_SETTINGS['MONGO_PORT'] = 61671
    EVE_SETTINGS['MONGO_USERNAME'] = 'ml-hackathon-g7'
    EVE_SETTINGS['MONGO_PASSWORD'] = '.hackathon.'
    EVE_SETTINGS['MONGO_DBNAME'] = 'heroku_app35780615'
else:
    EVE_SETTINGS['MONGO_DBNAME'] = 'melinder'

