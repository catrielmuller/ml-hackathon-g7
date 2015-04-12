import os
from flask.ext.cors import CORS
from melinder import app
cors = CORS(app)

port = os.environ.get('PORT')
if port:
    port = int(port)
else:
    port = 5000



app.secret_key = "\xe6\xd7\xcd2\x16\xb8\xa0,\x10\xb8V\xf8\xed\xa01\x9a\xbe\xfb\xa5\x88\xff\x0e\xd5"
app.run(host='0.0.0.0', port=port, debug=True)

