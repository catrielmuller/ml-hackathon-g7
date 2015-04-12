import settings
from eve import Eve

from components import initialize, users, categories, likes, offers, products
import os


PWD = os.environ.get('PWD')
STATIC_FOLDER = os.path.join(PWD, 'public')

app = Eve(settings=settings.EVE_SETTINGS, static_folder=STATIC_FOLDER)

initialize.initialize_components(app, [users, categories, likes, offers, products])


import login
import melinder.common
import melinder.buyer
import melinder.seller
