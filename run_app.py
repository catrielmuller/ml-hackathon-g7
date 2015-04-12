import os
from melinder import app
from melinder.callbacks import search_items, publish_clone

port = os.environ.get('PORT')
if port:
    port = int(port)
else:
    port = 5000

# cuando se hace un like, buscar los items en mercado libre
app.on_inserted_likes += search_items
# cuando un vendedor actualiza un precio, se publica un item clon
app.on_update_offers += publish_clone

app.secret_key = "\xe6\xd7\xcd2\x16\xb8\xa0,\x10\xb8V\xf8\xed\xa01\x9a\xbe\xfb\xa5\x88\xff\x0e\xd5"
app.run(host='0.0.0.0', port=port)

