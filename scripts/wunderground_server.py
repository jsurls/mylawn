import os
import json
from flask import Flask

app = Flask(__name__)


@app.route("/api/<apikey>/history_<date>/lang:EN/units:english/bestfct:1/v:2.0/q/<query>.json")
def get_history(apikey, date, query):
    with open("responses/sample_wunderground_history_response.json") as data_file:
        data = json.load(data_file)
        return json.dumps(data)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
