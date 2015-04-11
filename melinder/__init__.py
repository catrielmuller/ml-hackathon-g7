import settings
from eve import Eve

from components import initialize, users, categories
import os


PWD = os.environ.get('PWD')
STATIC_FOLDER = os.path.join(PWD, 'public')

app = Eve(settings=settings.EVE_SETTINGS, static_folder=STATIC_FOLDER)

print settings.EVE_SETTINGS

initialize.initialize_components(app, [users, categories])

import login
import melinder.views
