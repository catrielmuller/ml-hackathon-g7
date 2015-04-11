from flask import Flask
import settings
from eve import Eve
import pymongo

from components import initialize, users
import os


app = Eve(settings=settings.EVE_SETTINGS)
PWD = os.environ.get('PWD')
STATIC_FOLDER = os.path.join(PWD, 'public')

app = Eve(settings=settings.EVE_SETTINGS, static_folder=STATIC_FOLDER)

initialize.initialize_components(app, [users])

import login
import melinder.views
