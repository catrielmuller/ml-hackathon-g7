from flask import send_from_directory, current_app, request, session, redirect
import json

from eve.utils import parse_request

from melinder import app, STATIC_FOLDER
from login import meli, login_required


@app.route('/api/offer/<offer>/change_price/')
@login_required
def change_price():
    # chequear que <offer> sea de <me>
    # publicar un item igual a <offer>
    # devolver item
    #meli.get("/sites/MLA/search/?category=MLA5725&q=ipod", {'access_token': session['access_token']}).content
    return ""

