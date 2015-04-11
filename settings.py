import os
import sys

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
    print 'prod'
    sys.stdout.flush()
    EVE_SETTINGS['MONGO_HOST'] = 'ds061671.mongolab.com'
    EVE_SETTINGS['MONGO_PORT'] = 61671
    EVE_SETTINGS['MONGO_USERNAME'] = 'ml-hackathon-g7'
    EVE_SETTINGS['MONGO_PASSWORD'] = '.hackathon.'
    EVE_SETTINGS['MONGO_DBNAME'] = 'heroku_app35780615'

    EVE_SETTINGS['MONGO_URI'] = 'mongodb://ml-hackathon-g7:.hackathon.@ds061671.mongolab.com:61671/heroku_app35780615'
else:
    print 'local'
    sys.stdout.flush()
    EVE_SETTINGS['MONGO_DBNAME'] = 'melinder'

