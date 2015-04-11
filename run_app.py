import os

from melinder import app

app.secret_key = "\xe6\xd7\xcd2\x16\xb8\xa0,\x10\xb8V\xf8\xed\xa01\x9a\xbe\xfb\xa5\x88\xff\x0e\xd5"
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)

