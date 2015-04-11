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
    EVE_SETTINGS['MONGO_URI'] = os.environ.get('MONGOLAB_URI')
else:
    print 'local'
    sys.stdout.flush()
    EVE_SETTINGS['MONGO_DBNAME'] = 'melinder'

